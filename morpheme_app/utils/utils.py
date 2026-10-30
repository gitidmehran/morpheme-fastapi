from sqlalchemy.orm import Session
from ..models.MorphemeDetailNew_model import MorphemeDetailNew
from ..models.Word_model import Word
import requests
from fastapi import HTTPException
from time import sleep
# import boto3
# import os
from dotenv import load_dotenv

def get_words_by_morpheme(db: Session, root_word_id: int, data: dict):
    """Fetch morphemes by root word ID and additional filters."""
    return db.query(MorphemeDetailNew).filter_by(
        root_word_id=root_word_id,
        weight=data['weight'],
        morpheme_no=data['morpheme_no']
    ).all()


def get_morpheme_details(db: Session, root_word_id: int, weight: int = None, morpheme_no: int = None):
    """Fetch morpheme details with optional filters."""
    query = db.query(MorphemeDetailNew).filter_by(root_word_id=root_word_id)
    if weight is not None:
        query = query.filter_by(weight=weight)
    if morpheme_no is not None:
        query = query.filter_by(morpheme_no=morpheme_no)
    return query.all()


def get_words_by_morpheme_detail(db: Session, morpheme_detail_id: int, word_number: int = None):
    """Fetch words based on morpheme detail ID with an optional word number filter."""
    query = db.query(Word).filter_by(morpheme_detail_id=morpheme_detail_id)
    if word_number is not None:
        query = query.filter_by(word_number=word_number)
    return query.all()


def get_existing_root_word_ids(db: Session):
    """Fetch existing root word IDs from the MorphemeDetailNew table."""
    return db.query(MorphemeDetailNew.root_word_id).group_by(MorphemeDetailNew.root_word_id).all()


def get_quranic_data(retries=3, delay=2):
    """Fetch Quranic data with retries and error handling."""
    for attempt in range(retries):
        try:
            response = requests.get("https://rq-devlr.researchquran.org/api/get-quran-data", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise HTTPException(status_code=500, detail=f"Error fetching Quranic data: {e}")
            sleep(delay)


# Load environment variables from .env file
load_dotenv()

# # Define AWS credentials and bucket info
# BUCKET_NAME = os.getenv("BUCKET_NAME")
# AWS_URL = os.getenv("AWS_URL")
# ENDPOINT_URL = os.getenv("ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# REGION_NAME = os.getenv("REGION_NAME")

# if not all([BUCKET_NAME, AWS_URL, ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME]):
#     print("Error: One or more AWS configuration environment variables are not set.")

# def get_s3_client():
#     """Initialize and return an S3 client."""
#     return boto3.client(
#         's3',
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         region_name=REGION_NAME,
#         endpoint_url=ENDPOINT_URL
#     )