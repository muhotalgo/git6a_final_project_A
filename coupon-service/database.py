import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlmodels import Base

db_url = 'sqlite:///coupon.db'

engine = sqlalchemy.create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
