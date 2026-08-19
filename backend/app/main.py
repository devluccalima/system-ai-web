from app.core.config import settings
from app.core.database import get_db

# Imports dos routers
from app.routes import auth, chat, users
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

origins = [
    "http://localhost:4200",  # Adicione o endereço do frontend aqui
    "http://127.0.0.1:4200",  # Adicione o endereço do frontend aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Conversation-ID"],
)

app.include_router(users.router, prefix="/api/v1")  # Prefixo para a versão da API
app.include_router(auth.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")  # Prefixo para a versão da API


@app.get("/")
def read_root():
    return {"message": "SYSTEM API is running!"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Tenta executar uma query simples no PostgreSQL
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
