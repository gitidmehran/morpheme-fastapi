from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

# Morpheme_model
class Morpheme(Base):
    __tablename__ = 'morphemes'

    id = Column(Integer, primary_key=True, index=True)
    matching_words = Column(String)
    sheet_reference = Column(String)
    morpheme_form = Column(String)
    # Define relationships
    morpheme_details = relationship("MorphemeDetails", back_populates="morpheme")
    morpheme_details_new = relationship("MorphemeDetailNew", back_populates="morpheme")
    words = relationship("Word", back_populates="morpheme")

