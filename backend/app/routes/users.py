from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está em uso.",
        )

    # 2. Força o corte da senha em 72 caracteres de
    # forma manual para não quebrar o bcrypt
    senha_segura_truncada = user_in.password[:72]
    hashed_pwd = get_password_hash(senha_segura_truncada)

    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        name=user_in.name,
        ai_context=user_in.ai_context.model_dump(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário atualmente logado (Exige Token JWT)."""
    return current_user
