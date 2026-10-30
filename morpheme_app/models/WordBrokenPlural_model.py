from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


# WordBrokenPlural_model
class WordBrokenPlural(Base):
    __tablename__ = 'wordbrokenplural'

   # id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id'),primary_key=True)
    broken_plural_id = Column(Integer, ForeignKey('brokenplurals.id'))

    # Relationships
    broken_plural = relationship("BrokenPlural", back_populates="word_broken_plural")
    word = relationship("Word", back_populates="broken_plurals")

