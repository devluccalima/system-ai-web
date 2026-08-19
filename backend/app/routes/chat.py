# app/routes/chat.py
from app.core.database import SessionLocal, get_db
from app.core.deps import get_current_user
from app.core.llm import build_chat_payload
from app.models.chat import Conversation, Message
from app.schemas.chat import ChatRequest
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import ollama

router = APIRouter(prefix="/chat", tags=["Chat AI"])


@router.post("/")
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. Verifica se já estamos em uma conversa ou se cria uma nova
    if request.conversation_id:
        conv = (
            db.query(Conversation)
            .filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == current_user.id,
            )
            .first()
        )
    else:
        # Cria nova conversa usando as primeiras palavras como título
        conv = Conversation(user_id=current_user.id, title=request.message[:30] + "...")
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # 2. Salva a mensagem que o usuário acabou de enviar
    user_msg = Message(conversation_id=conv.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # 3. Puxa toda a história e monta o prompt
    history = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    messages_payload = build_chat_payload(current_user.ai_context, history)

    def generate():
        stream = ollama.chat(model="llama3.2", messages=messages_payload, stream=True)
        full_ai_response = ""

        for chunk in stream:
            content = chunk["message"]["content"]
            full_ai_response += content
            yield content

        # 4. SALVAMENTO SEGURO: Abre uma conexão rápida só para
        # salvar a resposta completa da IA
        db_gen = SessionLocal()
        try:
            ai_msg = Message(
                conversation_id=conv.id, role="assistant", content=full_ai_response
            )
            db_gen.add(ai_msg)
            db_gen.commit()
        finally:
            db_gen.close()

    # Devolvemos o stream, mas enviamos o ID da conversa escondido no Header!
    return StreamingResponse(
        generate(), media_type="text/plain", headers={"X-Conversation-ID": str(conv.id)}
    )


@router.get("/conversations")
async def list_conversations(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    """
    Retorna a lista de todas as conversas do usuário logado,
    ordenadas das mais recentes para as mais antigas.
    """
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    # Formatamos a saída para o Angular ler facilmente
    return [{"id": str(c.id), "title": c.title} for c in conversations]


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. Verifica se a conversa existe e pertence ao usuário logado (segurança)
    conv = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id, Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")

    # 2. Busca as mensagens em ordem cronológica
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    # 3. Retorna no formato exato que o Angular espera: { role: '...', content: '...' }
    return [{"role": m.role, "content": m.content} for m in messages]


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1. Busca a conversa garantindo que pertence ao usuário logado
    conv = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id, Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")

    # 2. Deleta a conversa (o SQLAlchemy/PostgreSQL se encarrega de
    # deletar as mensagens caso haja cascade)
    db.delete(conv)
    db.commit()

    return {"status": "success", "message": "Memória apagada com sucesso"}
