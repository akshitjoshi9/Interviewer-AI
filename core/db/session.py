from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine_ml = create_engine(
    settings.DATABASE_URL_ENGINE, 
    echo=False,
    pool_size=20,
    max_overflow=30,
    pool_timeout=60
    )

def get_session_ml_engine():
    session = Session(engine_ml)
    try:
        yield session
    finally:
        session.close()


SessionLocalML = sessionmaker(
    bind=engine_ml,
    autocommit=False,
    autoflush=False,
)