# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from models import Base, Executor, ContractType
from routes import router as crm_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Наполним начальными данными, если пусто
@app.on_event("startup")
def seed_data():
    db: Session = SessionLocal()
    try:
        if db.query(Executor).count() == 0:
            db.add_all([
                Executor(name_executor="Иван Петров"),
                Executor(name_executor="ООО «Альфа»"),
                Executor(name_executor="Мария Смирнова"),
            ])
        if db.query(ContractType).count() == 0:
            db.add_all([
                ContractType(contract_type_name="Договор А"),
                ContractType(contract_type_name="Договор Б"),
            ])
        db.commit()
    finally:
        db.close()

app.include_router(crm_router)
