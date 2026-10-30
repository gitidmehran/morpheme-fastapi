from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    morpheme_id = Column(Integer, ForeignKey('morphemes.id'))
    morpheme_detail_id = Column(Integer, ForeignKey('morpheme_details_new.id'))
    template_id = Column(Integer, ForeignKey('templates.id'))
    heading_id = Column(Integer, ForeignKey('headings.id'))
    subheading_id = Column(Integer, ForeignKey('subheadings.id'))

    morpheme_no = Column(Integer)
    weight = Column(Integer)
    word = Column(String)
    group = Column(String)
    subgroup = Column(String)
    word_number = Column(String)
    isbroken = Column(Integer)

    # Relationships
    morpheme = relationship("Morpheme", back_populates="words")
    morpheme_details = relationship("MorphemeDetailNew", back_populates="words")
    template = relationship("Template")
    heading = relationship("Heading")
    subheading = relationship("SubHeading")
    broken_plurals = relationship("WordBrokenPlural", back_populates="word")
