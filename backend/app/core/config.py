import os

from dotenv import load_dotenv

# Carrega as variaveis do arquivo .env
load_dotenv()


class Settings:
    PROJECT_NAME: str = "SYSTEM API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
