from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    price = Column(Numeric(10, 2))
    availability = Column(Boolean, default=True)