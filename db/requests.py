import datetime

from pydantic import BaseModel
from sqlalchemy import select

from db.data_base import Session, engine, Base
from db.models import Child_ORM, EmotionTest_ORM, RavenTest_ORM, RelationTest_ORM
from models import Applicant

class ApplicantCreate(BaseModel):
    last_name: str
    passport: str
    snils: str
    education: list[str]
    photo: str


def create_tables():
    Base.metadata.create_all(bind=engine)

def add_applicant():

    return applicant