from sqlalchemy import Column, Integer, String
from app.database import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    population = Column(Integer, nullable=False)
