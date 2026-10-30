from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


# RootWordSheet_model
class RootWordSheet(Base):
    __tablename__ = 'root_word_sheets'

    id = Column(Integer, primary_key=True, index=True)
