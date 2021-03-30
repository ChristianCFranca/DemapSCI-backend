from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URL = DATABASE_URL if DATABASE_URL else "sqlite:///./sql-demap-sci.db"

if not DATABASE_URL:
    print("DATABASE_URL is not set. Serving SQLite database.")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Precisa apenas para o SQLite
    )

else:
    print("DATABASE_URL available! Serving PostgreSQL database.")
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres", "postgresql") # Heroku use
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()