import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
load_dotenv(Path(__file__).resolve().parent.parent / '.env', override=True)
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
if SQLALCHEMY_DATABASE_URL.startswith('postgres'):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://').replace('postgres://', 'postgresql+psycopg://')
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
  