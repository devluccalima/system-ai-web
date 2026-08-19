# backend/app/core/llm.py


def build_chat_payload(ai_context_dict: dict, db_history: list):
    # 1. Monta as instruções base (System Prompt)
    system_prompt = (
        "Você é o SYSTEM, um assistente virtual objetivo e altamente capacitado."
    )
    if ai_context_dict:
        custom_inst = ai_context_dict.get("custom_instructions", "")
        if custom_inst:
            system_prompt += f"\nInstruções: {custom_inst}"
        prof = ai_context_dict.get("profession")
        if prof:
            system_prompt += f"\nProfissão do usuário: {prof}"

    messages = [{"role": "system", "content": system_prompt}]

    # 2. Injeta todo o histórico do banco de dados na memória do LLM
    for msg in db_history:
        # Garante que as mensagens da IA sejam lidas como 'assistant' (padrão do Llama)
        role = "assistant" if msg.role in ["system", "assistant"] else "user"
        messages.append({"role": role, "content": msg.content})

    return messages
