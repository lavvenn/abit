from sqlalchemy.orm import Mapped, mapped_column

from db.data_base import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    added_at: Mapped[str] = mapped_column()
    direction: Mapped[str] = mapped_column()
    level: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column(default=None)
    parent_phone_number: Mapped[str] = mapped_column(default=None)
    activaided: Mapped[bool] = mapped_column(default=True)
    aproved: Mapped[bool] = mapped_column(default=False)