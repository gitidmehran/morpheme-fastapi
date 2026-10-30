from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class BrokenPlural(Base):
    __tablename__ = 'brokenplurals'

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey('broken_plural_templates.id'))
    word = Column(String)

    # Relationships
    word_broken_plural = relationship("WordBrokenPlural", back_populates="broken_plural")
    template = relationship("BrokenPluralTemplate", back_populates="broken_plurals")
