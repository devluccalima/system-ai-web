# app/schemas/chat.py
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ..., description="A mensagem que o usuário digitou no frontend"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="O ID da conversa, se houver. Se não houver, "
        "será gerado um novo ID de conversa.",
    )


class ChatResponse(BaseModel):
    reply: str = Field(..., description="A resposta gerada pelo LLM")
