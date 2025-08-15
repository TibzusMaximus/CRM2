
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, ForeignKey

Base = declarative_base()

class Executor(Base):
    __tablename__ = "executors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name_executor: Mapped[str] = mapped_column(String, index=True)

class ContractType(Base):
    __tablename__ = "contract_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    contract_type_name: Mapped[str] = mapped_column(String, index=True)

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    executor_id: Mapped[int] = mapped_column(ForeignKey("executors.id"))
    contract_type_id: Mapped[int] = mapped_column(ForeignKey("contract_types.id"))
    contract_date: Mapped[Date] = mapped_column(Date)
    contract_number: Mapped[str] = mapped_column(String)
