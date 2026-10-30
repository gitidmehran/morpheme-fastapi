from pydantic import BaseModel, Field
from typing import List, Optional

class MorphemeData(BaseModel):
    weight: int
    morpheme_no: int
    word_number: str
    group: int
    subgroup: str

class DataItem(BaseModel):
    weight: int
    morpheme_no: int
    word_number: str
    
class MorphemeRequest(BaseModel):
    rootWord: str  # Required field for the root word
    data: List[DataItem] # Optional, default to an empty list
class MorphemesRequest(BaseModel):
    rootWord: str  # Required field for the root word
    data: List[MorphemeData] = []
    
class WordResponse(BaseModel):
    morpheme_no: int
    weight: int
    word: str
    group: str
    subgroup: str
    word_number: str  # Update to string
    isbroken: bool
    broken_plurals: List[str]  # Adjust as necessary
    template: str
    ar: str
    en: str
    sub_ar: str
    sub_en: str
    reference: Optional[str] = "" 
    word_id: Optional[int]
    matchingWords: Optional[List[dict]] = []

class MorphemeResponse(BaseModel):
    success: bool
    message: str
    totalRecords: int
    list: List[dict]  # List of morphemes

class WordGroup(BaseModel):
    key: str
    words: List[WordResponse]

class WordGroupsResponse(BaseModel):
    success: bool
    message: str
    list: List[WordGroup]
    

class FileUploadRequest(BaseModel):
    name: str
    root_word_id: int

class FileResponse(BaseModel):
    id: int
    name: str
    root_word_id: int
    file: str
    url: str

class ErrorResponse(BaseModel):
    error: str
    
    
class GrammerFiles(BaseModel):
    root_word_id: int
    file: str
    


# Request model for delete
class DeleteFileRequest(BaseModel):
    root_word_id: int
    
    
    
class MorphemeeRequest(BaseModel):
    rootWord: str

class MatchingWords(BaseModel):
    wordId: int
    reference: str

class WordData(BaseModel):
    morpheme_no: int
    weight: int
    word: str
    group: str
    subgroup: str
    word_number: str
    isbroken: bool
    broken_plurals: List[str]
    template: str
    ar: str
    en: str
    sub_ar: str
    sub_en: str
    reference: bool
    word_id: Optional[int]
    matchingWords: List[MatchingWords]

class MainWordResponse(BaseModel):
    key: str
    arabicHeading: str
    englishHeading: str
    words: List[WordData]

class SubGroupResponse(BaseModel):
    key: str
    referenceWordCount: int
    arabicHeading: str
    englishHeading: str
    mainWords: List[MainWordResponse]

class GroupResponse(BaseModel):
    key: str
    isReferenceExist: bool
    subGroups: List[SubGroupResponse]

class MorphemeData(BaseModel):
    weight: str
    morphemeForm: str
    isReferenceExist: bool
    groups: List[GroupResponse] = Field(default_factory=list)

class WordGroupssResponse(BaseModel):
    success: bool
    message: str
    list: List[MorphemeData]