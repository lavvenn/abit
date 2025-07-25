from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ABITS.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()