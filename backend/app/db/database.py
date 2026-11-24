from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


# Create database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class for SQLAlchemy models
Base = declarative_base()

def test_db_connection():
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
            return True

    except Exception as error:
        print(f"Database connection failed: {error}")
        return False


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
