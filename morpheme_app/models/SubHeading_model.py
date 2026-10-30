from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


# SubHeading_model
class SubHeading(Base):
    __tablename__ = 'subheadings'

    id = Column(Integer, primary_key=True, index=True)
    sub_ar  = Column(String(255))
    sub_en  = Column(String(255))