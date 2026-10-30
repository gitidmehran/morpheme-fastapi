from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class MorphemeDetailNew(Base):
    __tablename__ = 'morpheme_details_new'

    id = Column(Integer, primary_key=True, index=True)
    morpheme_id = Column(Integer, ForeignKey('morphemes.id'))
    root_word_id = Column(Integer)
    
    weight = Column(Integer)
    morpheme_no = Column(Integer)
    form = None
    # Relationships
    words = relationship("Word", back_populates="morpheme_details")
    morpheme = relationship("Morpheme", back_populates="morpheme_details_new")
