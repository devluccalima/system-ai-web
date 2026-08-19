from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

# --- ESTRUTURA DO ONBOARDING (O JSONB final) ---


class AIContext(BaseModel):
    # Predefinidos
    profession: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    hobbies: Optional[List[str]] = []
    current_projects: Optional[List[str]] = []
    custom_instructions: Optional[str] = None

    # Textos Manuais (Onde você vai digitar livremente)
    current_projects: List[str] = Field(
        default=[],
        description="Ex: ['Sistema de Controle de Gastos', 'Build de PC 2026']",
    )
    custom_instructions: Optional[str] = Field(
        default=None,
        description=(
            "Ex: 'Seja direto em assuntos de código, " "mas imersivo ao falar de RPG.'"
        ),
    )


# --- ESQUEMAS DE CRIAÇÃO E RESPOSTA DA API ---


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8, max_length=72, description="Senha deve ter minímo 8 caracteres."
    )
    name: str
    ai_context: AIContext


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    ai_context: AIContext
    is_active: bool

    class Config:
        from_attributes = True
