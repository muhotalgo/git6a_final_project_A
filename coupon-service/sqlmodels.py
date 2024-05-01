from datetime import datetime

from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Coupon(Base):
    __tablename__ = 'coupon'

    dno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cno = Column(String(20), nullable=False, unique=True)
    disc = Column(String(30), nullable=False)
    disc_time = Column(String(20), nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    usec = Column(String(3), nullable=False, default='n')
