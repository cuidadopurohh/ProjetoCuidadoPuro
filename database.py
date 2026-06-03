from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

RAW_URL = os.getenv("DATABASE_URL")
if not RAW_URL:
    raise RuntimeError(
        "DATABASE_URL não foi configurado. Defina DATABASE_URL no arquivo .env."
    )

# O SQLAlchemy precisa do driver psycopg2 explícito em URLs PostgreSQL
if RAW_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
elif RAW_URL.startswith("postgres://"):
    DATABASE_URL = RAW_URL.replace("postgres://", "postgresql+psycopg2://", 1)
else:
    DATABASE_URL = RAW_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()