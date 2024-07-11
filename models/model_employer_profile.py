from sqlalchemy import Column, Integer, String
from database import Base

class Employer_Profiles(Base):
    __tablename__ = 'Employer_Profiles'

    id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    employer_id = Column(Integer)  #To make Foreign key
    company_name = Column(String(20))
    company_description = Column(String(2000))
    website = Column(String(255))
    created_at = Column(String(20))
    updated_at = Column(String(20))






