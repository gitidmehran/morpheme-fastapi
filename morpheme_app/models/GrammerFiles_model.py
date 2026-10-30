from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


# GrammerFiles_model
class GrammerFiles(Base):
    __tablename__ = 'grammer_files'

    id = Column(Integer, primary_key=True, index=True)
    root_word_id = Column(Integer)
    name = Column(String, index=True)
    file = Column(String)