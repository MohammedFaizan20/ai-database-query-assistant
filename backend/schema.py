# backend/schema.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    salary: float
