# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from models import Base, Executor, ClientType, SampleContract
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
        if db.query(ClientType).count() == 0:
            db.add(ClientType(id_type_client=1, id_type_short="ООО", id_type_long="Общество с ограниченной ответственностью"))
        if db.query(Executor).count() == 0:
            db.add(Executor(
                id_executor="executor1",
                type_executor=1,
                name_executor="Иван Петров",
                inn_executor="1234567890",
                ogrn_executor="1234567890123",
                kpp_executor=None,
                adress_executor="Адрес",
                bank_executor="Банк",
                cor_bank_executor="12345678901234567890",
                acc_bank_executor="12345678901234567890",
                bik_bank_executor="123456789",
                contact_name_executor="Иван Петров",
                mail_executor="ivan@example.com",
                tel_executor="1234567890",
                mess_executor="Telegram",
            ))
        if db.query(SampleContract).count() == 0:
            db.add(SampleContract(
                id_sample_contract="sample_contract1",
                name_sample_contract="Договор А",
                path_sample_contract="/docs/contract_a.doc",
            ))
        db.commit()
    finally:
        db.close()

app.include_router(crm_router)
