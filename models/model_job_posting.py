from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
# from model_employer import Employers

class Job_Postings(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    # employer_id = Column(Integer) #To make Foreign key  
    employer_id = Column(Integer, ForeignKey("employers.id", ondelete="CASCADE")) 
    
    job_type = Column(String(20))
    job_title = Column(String(100))
    job_description = Column(String(1000))
    no_of_positions = Column(Integer)
    skills = Column(String(100))
    location = Column(String(50))
    salary = Column(Integer)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    apply_before = Column(String(20))
