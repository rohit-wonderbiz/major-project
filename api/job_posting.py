
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_job_posting import Job_Postings
from database import Sessionlocal

job_posting = APIRouter()

class Job_PostingsBase(BaseModel):
    employer_id: int #To make Foreign key  
    job_type: str
    job_title: str
    job_description: str
    no_of_positions: int
    skills: str
    location: str
    salary: int
    apply_before: str

class Job_PostingsCreate(Job_PostingsBase):
    pass

class Job_PostingsRead(Job_PostingsBase):
    id: int
    posted_at: datetime

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
@job_posting.get("/job/", response_model=list[Job_PostingsRead], status_code=status.HTTP_200_OK)
async def read_all_employee(db: db_dependency):
    employee_profiles = db.query(Job_Postings).all()
    if not employee_profiles:
        raise HTTPException(status_code=404, detail='No employee profiles were found')
    return employee_profiles

# Employers Table GET Method
@job_posting.get("/job/{emp_Id}", response_model=Job_PostingsRead, status_code=status.HTTP_200_OK)
async def read_employee(emp_Id: int, db: db_dependency):
    post = db.query(Job_Postings).filter(Job_Postings.id == emp_Id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    return post

# Employers Table POST Method
@job_posting.post("/job/", response_model=Job_PostingsRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: Job_PostingsCreate, db: db_dependency):
    db_post = Job_Postings(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Employers Table DELETE Method
@job_posting.delete("/job/{emp_Id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_Id: int, db: db_dependency):
    db_post = db.query(Job_Postings).filter(Job_Postings.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    db.delete(db_post)
    db.commit()

# Employers Table EDIT Method
@job_posting.put("/job/{emp_Id}", response_model=Job_PostingsRead, status_code=status.HTTP_200_OK)
async def update_employee(emp_Id: int, updated_post: Job_PostingsCreate, db: db_dependency):
    db_post = db.query(Job_Postings).filter(Job_Postings.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post
