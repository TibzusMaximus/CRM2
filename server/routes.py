from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from db import SessionLocal
from models import Executor, ClientType, SampleContract, Client

router = APIRouter(prefix="/api", tags=["crm"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ExecutorOut(BaseModel):
    class Config:
        from_attributes = True


class SampleContractOut(BaseModel):
    id_sample_contract: str
    name_sample_contract: str

    class Config:
        from_attributes = True


class ClientTypeOut(BaseModel):
    id_type_client: int
    id_type_long: str

    class Config:
        from_attributes = True

class ClientIn(BaseModel):
    type_client: int
    inn_client: str
    ogrn_client: str
    kpp_client: str | None = None
    name_client: str
    adress_client: str
    bank_client: str
    bik_bank_client: str
    acc_bank_client: str
    cor_bank_client: str
    tel_client: str
    mail_client: str
    mess_client: str
    contact_name_client: str


class ClientOut(ClientIn):
    id_client: str

    class Config:
        from_attributes = True


@router.get("/executors", response_model=list[ExecutorOut])
def list_executors(db: Session = Depends(get_db)):
    return db.query(Executor).order_by(Executor.name_executor).all()

@router.get("/sample-contracts", response_model=list[SampleContractOut])
def list_sample_contracts(db: Session = Depends(get_db)):
    return db.query(SampleContract).order_by(SampleContract.name_sample_contract).all()


@router.get("/client-types", response_model=list[ClientTypeOut])
def list_client_types(db: Session = Depends(get_db)):
    return db.query(ClientType).order_by(ClientType.id_type_long).all()


@router.post("/clients", response_model=ClientOut, status_code=201)
def create_client(payload: ClientIn, db: Session = Depends(get_db)):
     client = Client(id_client=f"client{uuid.uuid4().hex}", **payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
