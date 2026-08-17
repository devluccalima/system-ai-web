import jwt
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Informa ao FastAPI qual é a rota que gera os tokens (usado pelo Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Verifica se o token é válido e retorna o usuário logado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais (Token inválido ou expirado)",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Descriptografa o token usando nossa chave secreta
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:  # Captura qualquer erro do JWT (expirado, alterado, etc)
        raise credentials_exception

    # Busca o usuário no banco para garantir que ele ainda existe/está ativo
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
