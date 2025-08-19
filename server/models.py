"""
CRM models (PostgreSQL, SQLAlchemy 2.0)

Сущности:
- client_types
- clients
- executors
- sample_contracts, sample_attaches
- services
- deals
- attachments

Принципы:
- Строковые PK с обязательным префиксом (client..., executor..., deal..., attachment..., service..., sample_contract..., sample_attach...).
- Идентификаторы/реквизиты "число фиксированной длины" — храним как TEXT/STRING + CHECK (только цифры и длина), чтобы не терять ведущие нули.
- Даты: DATE.
- Удаление родителя запрещено при наличии детей (RESTRICT), кроме каскада шаблонов: удаление шаблона договора удаляет его шаблоны приложений (CASCADE).
"""

from __future__ import annotations
from typing import Optional
from datetime import date
from sqlalchemy import (
    CheckConstraint, ForeignKey, UniqueConstraint, Text, SmallInteger,
    String, Date, Numeric, Boolean
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# =================== Base ===================
class Base(DeclarativeBase):
    pass


# ============ Типы клиентов (1..9) ============
class ClientType(Base):
    __tablename__ = "client_types"
    __table_args__ = (
        CheckConstraint("id_type_client BETWEEN 1 AND 9", name="ck_client_types_id_range"),
        UniqueConstraint("id_type_short", name="uq_client_types_short"),
        UniqueConstraint("id_type_long",  name="uq_client_types_long"),
    )

    id_type_client: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    id_type_short: Mapped[Optional[str]] = mapped_column(Text)  # может быть NULL
    id_type_long:  Mapped[Optional[str]] = mapped_column(Text)

    clients:   Mapped[list["Client"]]   = relationship(back_populates="type_ref")
    executors: Mapped[list["Executor"]] = relationship(back_populates="type_ref")

    def __repr__(self) -> str:
        return f"<ClientType {self.id_type_client} {self.id_type_short!r}>"


# =================== Клиенты ===================
class Client(Base):
    __tablename__ = "clients"
    __table_args__ = (
        CheckConstraint("id_client LIKE 'client%'", name="ck_clients_id_prefix"),
        CheckConstraint("(inn_client ~ '^[0-9]{10,12}$')", name="ck_clients_inn_digits_len"),
        CheckConstraint("(ogrn_client ~ '^[0-9]{13,15}$')", name="ck_clients_ogrn_digits_len"),
        CheckConstraint("(kpp_client IS NULL) OR (kpp_client ~ '^[0-9]{9}$')", name="ck_clients_kpp_digits_len"),
        CheckConstraint("(cor_bank_client ~ '^[0-9]{20}$')",  name="ck_clients_cor_bank_20"),
        CheckConstraint("(acc_bank_client ~ '^[0-9]{20}$')",  name="ck_clients_acc_bank_20"),
        CheckConstraint("(bik_bank_client ~ '^[0-9]{9}$')",   name="ck_clients_bik_9"),
    )

    id_client: Mapped[str] = mapped_column(String(128), primary_key=True)
    type_client: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("client_types.id_type_client", ondelete="RESTRICT"),
        nullable=False
    )

    name_client:   Mapped[str]          = mapped_column(Text, nullable=False)
    inn_client:    Mapped[str]          = mapped_column(String(15), nullable=False)
    ogrn_client:   Mapped[str]          = mapped_column(String(18), nullable=False)
    kpp_client:    Mapped[Optional[str]] = mapped_column(String(9))
    adress_client: Mapped[str]          = mapped_column(Text, nullable=False)

    bank_client:     Mapped[str] = mapped_column(Text, nullable=False)
    cor_bank_client: Mapped[str] = mapped_column(String(20), nullable=False)
    acc_bank_client: Mapped[str] = mapped_column(String(20), nullable=False)
    bik_bank_client: Mapped[str] = mapped_column(String(9),  nullable=False)

    contact_name_client: Mapped[str] = mapped_column(Text, nullable=False)
    mail_client:         Mapped[str] = mapped_column(Text, nullable=False)
    tel_client:          Mapped[str] = mapped_column(Text, nullable=False)
    mess_client:         Mapped[str] = mapped_column(Text, nullable=False)

    type_ref: Mapped["ClientType"] = relationship(back_populates="clients")

    # deals класть необязательно, но полезно:
    deals: Mapped[list["Deal"]] = relationship(back_populates="client")

    def __repr__(self) -> str:
        return f"<Client {self.id_client} {self.name_client!r} type={self.type_client}>"


# ================== Исполнители ==================
class Executor(Base):
    __tablename__ = "executors"
    __table_args__ = (
        CheckConstraint("id_executor LIKE 'executor%'", name="ck_executors_id_prefix"),
        CheckConstraint("(inn_executor ~ '^[0-9]{10,12}$')", name="ck_executors_inn_digits_len"),
        CheckConstraint("(ogrn_executor ~ '^[0-9]{13,15}$')", name="ck_executors_ogrn_digits_len"),
        CheckConstraint("(kpp_executor IS NULL) OR (kpp_executor ~ '^[0-9]{9}$')", name="ck_executors_kpp_digits_len"),
        CheckConstraint("(cor_bank_executor ~ '^[0-9]{20}$')",  name="ck_executors_cor_bank_20"),
        CheckConstraint("(acc_bank_executor ~ '^[0-9]{20}$')",  name="ck_executors_acc_bank_20"),
        CheckConstraint("(bik_bank_executor ~ '^[0-9]{9}$')",   name="ck_executors_bik_9"),
    )

    id_executor: Mapped[str] = mapped_column(String(128), primary_key=True)
    type_executor: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("client_types.id_type_client", ondelete="RESTRICT"),  # используем те же типы 1..9
        nullable=False
    )

    name_executor:   Mapped[str]           = mapped_column(Text, nullable=False)
    inn_executor:    Mapped[str]           = mapped_column(String(15), nullable=False)
    ogrn_executor:   Mapped[str]           = mapped_column(String(18), nullable=False)
    kpp_executor:    Mapped[Optional[str]] = mapped_column(String(9))
    adress_executor: Mapped[str]           = mapped_column(Text, nullable=False)

    bank_executor:     Mapped[str] = mapped_column(Text, nullable=False)
    cor_bank_executor: Mapped[str] = mapped_column(String(20), nullable=False)
    acc_bank_executor: Mapped[str] = mapped_column(String(20), nullable=False)
    bik_bank_executor: Mapped[str] = mapped_column(String(9),  nullable=False)

    contact_name_executor: Mapped[str] = mapped_column(Text, nullable=False)
    mail_executor:         Mapped[str] = mapped_column(Text, nullable=False)
    tel_executor:          Mapped[str] = mapped_column(Text, nullable=False)
    mess_executor:         Mapped[str] = mapped_column(Text, nullable=False)

    type_ref: Mapped["ClientType"] = relationship(back_populates="executors")

    deals: Mapped[list["Deal"]] = relationship(back_populates="executor")

    def __repr__(self) -> str:
        return f"<Executor {self.id_executor} {self.name_executor!r} type={self.type_executor}>"


# ============== Шаблоны договоров/приложений ==============
class SampleContract(Base):
    __tablename__ = "sample_contracts"
    __table_args__ = (
        CheckConstraint("id_sample_contract LIKE 'sample_contract%'", name="ck_sample_contract_id_prefix"),
    )

    id_sample_contract:  Mapped[str] = mapped_column(String(128), primary_key=True)
    name_sample_contract: Mapped[str] = mapped_column(Text, nullable=False)
    path_sample_contract: Mapped[str] = mapped_column(Text, nullable=False)  # путь к .doc

    sample_attaches: Mapped[list["SampleAttach"]] = relationship(
        back_populates="contract_tpl",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<SampleContract {self.id_sample_contract} {self.name_sample_contract!r}>"


class SampleAttach(Base):
    __tablename__ = "sample_attaches"
    __table_args__ = (
        CheckConstraint("id_sample_attach LIKE 'sample_attach%'", name="ck_sample_attach_id_prefix"),
    )

    id_sample_attach: Mapped[str] = mapped_column(String(128), primary_key=True)

    id_sample_attach_contract: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("sample_contracts.id_sample_contract", ondelete="CASCADE"),
        nullable=False
    )

    name_sample_attach: Mapped[str] = mapped_column(Text, nullable=False)
    path_sample_attach: Mapped[str] = mapped_column(Text, nullable=False)  # путь к .doc

    contract_tpl: Mapped["SampleContract"] = relationship(back_populates="sample_attaches")

    def __repr__(self) -> str:
        return f"<SampleAttach {self.id_sample_attach} -> {self.id_sample_attach_contract}>"


# ================= Номенклатура услуг =================
class Service(Base):
    __tablename__ = "services"
    __table_args__ = (
        CheckConstraint("id_service LIKE 'service%'", name="ck_service_id_prefix"),
    )

    id_service: Mapped[str] = mapped_column(String(128), primary_key=True)
    name_service: Mapped[str] = mapped_column(Text, nullable=False)

    # ссылка на применимый шаблон договора
    id_contract_service: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("sample_contracts.id_sample_contract", ondelete="RESTRICT"),
        nullable=False
    )

    contract_tpl: Mapped["SampleContract"] = relationship()
    attachments:  Mapped[list["Attachment"]] = relationship(back_populates="service")

    def __repr__(self) -> str:
        return f"<Service {self.id_service} {self.name_service!r}>"


# =================== Заключённые договоры ===================
class Deal(Base):
    __tablename__ = "deals"
    __table_args__ = (
        CheckConstraint("id_deal LIKE 'deal%'", name="ck_deals_id_prefix"),
        # номер договора — только цифры (сохраним как строку, чтобы не терять ведущие нули)
        CheckConstraint("(number_deal ~ '^[0-9]+$')", name="ck_deals_number_digits"),
    )

    id_deal: Mapped[str] = mapped_column(String(128), primary_key=True)

    id_client_deal: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("clients.id_client", ondelete="RESTRICT"),
        nullable=False
    )
    id_executor_deal: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("executors.id_executor", ondelete="RESTRICT"),
        nullable=False
    )

    number_deal: Mapped[str] = mapped_column(String(64), nullable=False)  # "число" в строке (для ведущих нулей)
    date_deal:   Mapped[date] = mapped_column(Date, nullable=False)       # ДД.ММ.ГГГГ → DATE

    # Статусы — вычисляемые бизнес-логикой; в БД храним как флаги
    status_deal:     Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    path_doc_deal:   Mapped[str]  = mapped_column(Text, nullable=False)   # путь к .doc
    path_pdf_deal:   Mapped[str]  = mapped_column(Text, nullable=False)   # путь к .pdf
    path_sign_deal:  Mapped[str]  = mapped_column(Text, nullable=True)    # путь к подписанному .pdf (может быть пусто)
    status_orig_deal: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    client:   Mapped["Client"]   = relationship(back_populates="deals")
    executor: Mapped["Executor"] = relationship(back_populates="deals")
    attachments: Mapped[list["Attachment"]] = relationship(back_populates="deal")

    def __repr__(self) -> str:
        return f"<Deal {self.id_deal} number={self.number_deal} date={self.date_deal}>"


# ============== Приложения к договору (Attachment) ==============
class Attachment(Base):
    __tablename__ = "attachments"
    __table_args__ = (
        CheckConstraint("id_attachment LIKE 'attachment%'", name="ck_attachment_id_prefix"),
        # дата окончания не раньше даты начала
        CheckConstraint("(date_end_attachment >= date_start_attachment)", name="ck_attachment_dates_order"),
        # цена — число с 2 знаками после запятой (на уровне БД NUMERIC, на уровне формата — в приложении)
    )

    id_attachment: Mapped[str] = mapped_column(String(128), primary_key=True)

    id_attachment_deal: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("deals.id_deal", ondelete="CASCADE"),
        nullable=False
    )
    id_service_attachment: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("services.id_service", ondelete="RESTRICT"),
        nullable=False
    )

    date_start_attachment: Mapped[date] = mapped_column(Date, nullable=False)
    date_end_attachment:   Mapped[date] = mapped_column(Date, nullable=False)

    place_attachment: Mapped[str] = mapped_column(Text, nullable=False)

    # Стоимость — число
    price_attachment: Mapped[Optional[float]] = mapped_column(Numeric(14, 2))  # можно NULL, если не указано

    path_doc_attachment:  Mapped[str] = mapped_column(Text, nullable=False)  # путь к .doc
    path_pdf_attachment:  Mapped[str] = mapped_column(Text, nullable=False)  # путь к .pdf
    path_sign_attachment: Mapped[Optional[str]] = mapped_column(Text)        # путь к подписанному .pdf (может быть пусто)

    # Статусы (вычисляет бэкенд):
    # - status_sign_attachment: True, если по path_sign_attachment реально есть .pdf
    # - status_attachment: True, если услуга ещё активна (текущая дата <= date_end_attachment)
    status_sign_attachment: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    status_attachment:      Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    deal:    Mapped["Deal"]    = relationship(back_populates="attachments")
    service: Mapped["Service"] = relationship(back_populates="attachments")

    def __repr__(self) -> str:
        return f"<Attachment {self.id_attachment} deal={self.id_attachment_deal} service={self.id_service_attachment}>"
