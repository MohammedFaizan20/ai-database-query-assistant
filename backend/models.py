# backend/models.py
from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    salary = Column(Float)