from app.core.config import settings
from app.core.database import get_db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


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
