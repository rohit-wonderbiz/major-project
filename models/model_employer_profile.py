from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Employer_Profiles(Base):
    __tablename__ = 'Employer_Profiles'

    id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    employer_id = Column(Integer)  #To make Foreign key
    company_name = Column(String(20))
    company_description = Column(String(2000))
    website = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())






