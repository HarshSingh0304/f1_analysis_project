from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from src.config import Config

def get_engine():
    Config.validate()

    url = (
        f"postgresql+psycopg2://{Config.DB_USER}:"
        f"{Config.DB_PASSWORD}@{Config.DB_HOST}:"
        f"{Config.DB_PORT}/{Config.DB_NAME}"
    )

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )
    return engine
