
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite файл в текущей папке. Можно заменить на Postgres DSN.
engine = create_engine("sqlite:///./crm.db", future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
