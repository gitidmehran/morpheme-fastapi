from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class BrokenPluralTemplate(Base):
    __tablename__ = 'broken_plural_templates'

    id = Column(Integer, primary_key=True, index=True)
    broken_plurals = relationship("BrokenPlural", back_populates="template")
    template_text = Column(String)
