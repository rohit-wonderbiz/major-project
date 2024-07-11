from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_employer_profile import Employer_Profiles
from database import Sessionlocal

employer_profile = APIRouter()

class Employer_ProfilesBase(BaseModel):
    employer_id: int  #To make Foreign key
    company_name: str
    company_description:str
    website: str
    created_at: str
    updated_at: str

class Employers_ProfilesCreate(Employer_ProfilesBase):
    pass

class Employers_ProfilesRead(Employer_ProfilesBase):
    id: int

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
@employer_profile.get("/employer_profile/", response_model=list[Employers_ProfilesRead], status_code=status.HTTP_200_OK)
async def read_all_employee(db: db_dependency):
    employee_profiles = db.query(Employer_Profiles).all()
    if not employee_profiles:
        raise HTTPException(status_code=404, detail='No employee profiles were found')
    return employee_profiles

# Employers Table GET Method
@employer_profile.get("/employer_profile/{emp_Id}", response_model=Employers_ProfilesRead, status_code=status.HTTP_200_OK)
async def read_employee(emp_Id: int, db: db_dependency):
    post = db.query(Employer_Profiles).filter(Employer_Profiles.id == emp_Id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    return post

# Employers Table POST Method
@employer_profile.post("/employer_profile/", response_model=Employers_ProfilesRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: Employers_ProfilesCreate, db: db_dependency):
    db_post = Employer_Profiles(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Employers Table DELETE Method
@employer_profile.delete("/employer_profile/{emp_Id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_Id: int, db: db_dependency):
    db_post = db.query(Employer_Profiles).filter(Employer_Profiles.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    db.delete(db_post)
    db.commit()

# Employers Table EDIT Method
@employer_profile.put("/employer_profile/{emp_Id}", response_model=Employers_ProfilesRead, status_code=status.HTTP_200_OK)
async def update_employee(emp_Id: int, updated_post: Employers_ProfilesCreate, db: db_dependency):
    db_post = db.query(Employer_Profiles).filter(Employer_Profiles.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post
