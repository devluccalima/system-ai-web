from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria o motor de conexao com o banco de dados
engine = create_engine(settings.DATABASE_URL)

# Cria a fabrica de sessoes para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os nossos modelos de banco de dados
Base = declarative_base()


# Funcao para injetar a sessao do banco nas rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
