from sqlalchemy import Column, Integer, String
from database import Base

class City(Base):
    __tablename__ = "cities"
    # primary_key=True:
    # Uniqueness --> No two rows can share this value
    # NOT NULL --> every row must have a value for this column
    
    # index=True
    # Quicker lookup --> tells database --> add an index on this column so lookups are faster
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
