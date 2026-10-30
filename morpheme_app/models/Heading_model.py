from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


# Heading_model
class Heading(Base):
    __tablename__ = 'headings'

    id = Column(Integer, primary_key=True, index=True)
    ar  = Column(String(255))
    en  = Column(String(255))