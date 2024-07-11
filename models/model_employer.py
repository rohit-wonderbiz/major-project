from sqlalchemy import Column, Integer, String
from database import Base

class Employers(Base):
    __tablename__ = 'Employers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    phone = Column(Integer)
    address = Column(String(255))
    created_at = Column(String(20))
    updated_at = Column(String(20))







