
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime, date
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Executor, ContractType, Client

router = APIRouter(prefix="/api", tags=["crm"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OUT-схемы
class ExecutorOut(BaseModel):
    id: int
    name_executor: str
    class Config: from_attributes = True

class ContractTypeOut(BaseModel):
    id: int
    contract_type_name: str
    class Config: from_attributes = True

# IN и OUT для клиента
class ClientIn(BaseModel):
    executor_id: int
    contract_type_id: int
    contract_date: str      # принимаем "dd.mm.yyyy" или ISO
    contract_number: str

    @field_validator("contract_date")
    @classmethod
    def normalize_date(cls, v: str) -> str:
        try:
            if "." in v:
                d = datetime.strptime(v, "%d.%m.%Y").date()
            else:
                d = datetime.fromisoformat(v).date()
            return d.isoformat()
        except Exception:
            raise ValueError("Неверный формат даты (используйте dd.mm.yyyy или yyyy-mm-dd)")

class ClientOut(BaseModel):
    id: int
    executor_id: int
    contract_type_id: int
    contract_date: date
    contract_number: str
    class Config: from_attributes = True

@router.get("/executors", response_model=list[ExecutorOut])
def list_executors(db: Session = Depends(get_db)):
    return db.query(Executor).order_by(Executor.name_executor).all()

@router.get("/contract-types", response_model=list[ContractTypeOut])
def list_contract_types(db: Session = Depends(get_db)):
    return db.query(ContractType).order_by(ContractType.contract_type_name).all()

@router.post("/clients", response_model=ClientOut, status_code=201)
def create_client(payload: ClientIn, db: Session = Depends(get_db)):
    if not db.get(Executor, payload.executor_id):
        raise HTTPException(400, "Executor not found")
    if not db.get(ContractType, payload.contract_type_id):
        raise HTTPException(400, "Contract type not found")

    client = Client(
        executor_id=payload.executor_id,
        contract_type_id=payload.contract_type_id,
        contract_date=datetime.fromisoformat(payload.contract_date).date(),
        contract_number=payload.contract_number,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
