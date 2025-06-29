from sqlalchemy.orm import Mapped, mapped_column

from db.data_base import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    added_at: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    passport: Mapped[str] = mapped_column()
    snils: Mapped[str] = mapped_column()
    education: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()