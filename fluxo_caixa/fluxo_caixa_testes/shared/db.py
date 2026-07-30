from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .config import get_settings

settings = get_settings()

# Use RDS Proxy endpoint in DATABASE_URL in AWS.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
