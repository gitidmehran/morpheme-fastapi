from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

# MorphemeDetail_model
class MorphemeDetails(Base):
    __tablename__ = 'morpheme_details'

    id = Column(Integer, primary_key=True, index=True)
    sheet_words = Column(String(255))
    root_word_id = Column(Integer)

    # Foreign key reference to the Morpheme model
    morpheme_id = Column(Integer, ForeignKey('morphemes.id'))  # Ensure this line exists

    # Define relationship back to Morpheme
    morpheme = relationship("Morpheme", back_populates="morpheme_details")

