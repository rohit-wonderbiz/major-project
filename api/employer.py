from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_employer import Employers
from database import Sessionlocal

employer = APIRouter()

class EmployersBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone: int
    address: str

class EmployersCreate(EmployersBase):
    pass

class EmployersRead(EmployersBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Employers Table GET Method ALL
@employer.get("/employer/", response_model=list[EmployersRead], status_code=status.HTTP_200_OK)
async def read_all_employee(db: db_dependency):
    employee_profiles = db.query(Employers).all()
    if not employee_profiles:
        raise HTTPException(status_code=404, detail='No employee profiles were found')
    return employee_profiles

# Employers Table GET Method
@employer.get("/employer/{emp_Id}", response_model=EmployersRead, status_code=status.HTTP_200_OK)
async def read_employee(emp_Id: int, db: db_dependency):
    post = db.query(Employers).filter(Employers.id == emp_Id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    return post

# Employers Table POST Method
@employer.post("/employer/", response_model=EmployersRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployersCreate, db: db_dependency):
    db_post = Employers(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Employers Table DELETE Method
@employer.delete("/employer/{emp_Id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_Id: int, db: db_dependency):
    db_post = db.query(Employers).filter(Employers.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    db.delete(db_post)
    db.commit()

# Employers Table EDIT Method
@employer.put("/employer/{emp_Id}", response_model=EmployersRead, status_code=status.HTTP_200_OK)
async def update_employee(emp_Id: int, updated_post: EmployersCreate, db: db_dependency):
    db_post = db.query(Employers).filter(Employers.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post
