from sqlalchemy import Column, Integer, BigInteger, String
from app.database import Base

class Country(Base):
    __tablename__ = "countries3"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    population = Column(BigInteger, nullable=False)
