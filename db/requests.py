import datetime

from pydantic import BaseModel
from sqlalchemy import select

from db.data_base import Session, engine, Base
from db.models import Applicant

class ApplicantCreate(BaseModel):
    last_name: str
    passport: str
    snils: str
    education: list[str]
    photo: str


def create_tables():
    Base.metadata.create_all(bind=engine)

def add_applicant(last_name: str, email: str,level: str, direction: str, phone_number: str = None, parent_phone_number: str = None) -> Applicant:
    session = Session()
    applicant = Applicant(
        added_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_name=last_name,
        email=email,
        level=level,
        direction=direction,
        phone_number=phone_number,
        parent_phone_number=parent_phone_number,
        activaided=False,
        aproved=False
    )
    session.add(applicant)
    session.commit()
    session.refresh(applicant)


    return "Applicant added successfully: " + applicant.last_name


def get_applicant_by_last_name(last_name: str) -> Applicant:
    session = Session()
    stmt = select(Applicant).where(Applicant.last_name == last_name)
    result = session.execute(stmt).scalars().first()
    session.close()
    
    if result:
        return result
    else:
        return None
    

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
    
    