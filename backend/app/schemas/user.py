from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

# --- OPÇÕES PREDEFINIDAS (Dropdowns e Checkboxes no Angular) ---


class TechInterest(str, Enum):
    PYTHON = "Python"
    ANGULAR = "Angular"
    REACT = "React"
    SQL = "SQL"
    POWER_APPS = "Power Apps"
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
    JAVA = "Java"
    DOTNET = ".NET"
    PHP = "PHP"
    AI = "Inteligência Artificial"
    OTHER = "Other"


class HobbyInterest(str, Enum):
    TABLETOP_RPG = "Tabletop RPGs"
    PC_GAMING = "PC Gaming"
    ANIME = "Anime & Manga"
    CARS = "Car Modification"
    TATTOOS = "Tattoo Aesthetics"
    FINANCE = "Personal Finance"
    CARTOONS = "Cartoons & Animation"
    IDEAS = "IDEAS (Inventions, Projects, Startups)"
    OTHER = "Other"


class ProfessionRole(str, Enum):
    IT_TECHNICIAN = "IT Technician"
    SOFTWARE_DEVELOPER = "Software Developer"
    STUDENT = "Student"
    ARCHITECT = "Architect"
    ENGINEER = "Engineer"
    LAWYER = "Lawyer"
    PSICHOLOGIST = "Psychologist"
    MUSICIAN = "Musician"
    ADMINISTRATOR = "Administrator"
    ACCOUNTANT = "Accountant"
    OTHER = "Other"


# --- ESTRUTURA DO ONBOARDING (O JSONB final) ---


class AIContext(BaseModel):
    # Predefinidos
    profession: ProfessionRole
    tech_stack: List[TechInterest] = []
    hobbies: List[HobbyInterest] = []

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
