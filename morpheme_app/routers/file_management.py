# from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
# from sqlalchemy.orm import Session
# from ..config.db_config import get_db
# from ..models.GrammerFiles_model import GrammerFiles
# from ..utils.utils import get_s3_client
# from typing import Optional
# import os


# # Router setup
# file_management_router = APIRouter(prefix="/api", tags=["File Management"])

# BUCKET_NAME = os.getenv("BUCKET_NAME")
# AWS_URL = os.getenv("AWS_URL")
# ENDPOINT_URL = os.getenv("ENDPOINT_URL")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# REGION_NAME = os.getenv("REGION_NAME")

# # Upload file to S3
# def upload_file_to_s3(file: UploadFile, file_name: str, old_file: Optional[str] = None) -> str:
#     s3 = get_s3_client()

#     # Remove old file if present
#     if old_file:
#         try:
#             s3.delete_object(Bucket=BUCKET_NAME, Key=old_file)
#         except s3.exceptions.NoSuchKey:
#             pass  # Handle cases where the old file doesn't exist in S3

#     # Ensure file is valid before upload
#     if not file.file:
#         raise HTTPException(status_code=400, detail="Uploaded file is invalid or empty.")

#     # Upload new file
#     s3.upload_fileobj(file.file, BUCKET_NAME, file_name)

#     # Return the URL to access the file
#     return f"{AWS_URL}/{file_name}"

# # Route for uploading a file
# @file_management_router.post("/upload-file", summary="Upload File")
# async def upload_file(
#     file: UploadFile = File(...),
#     root_word_id: int = Query(...),
#     name: str = Query(...),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Validate file type
#         valid_extensions = ['.pdf', '.doc', '.docx', '.xlsx']
#         file_extension = os.path.splitext(file.filename)[1].lower()
#         if file_extension not in valid_extensions:
#             raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed types: {', '.join(valid_extensions)}")

#         # Check if a file already exists for the root_word_id
#         existing_file = db.query(GrammerFiles).filter(GrammerFiles.root_word_id == root_word_id).first()

#         if existing_file:
#             # Update existing file
#             old_file = existing_file.file
#             new_file_path = upload_file_to_s3(file, name, old_file)

#             # Update database record
#             existing_file.name = name
#             existing_file.file = new_file_path
#             db.commit()

#             return {
#                 "id": existing_file.id,
#                 "name": name,
#                 "root_word_id": root_word_id,
#                 "file": new_file_path,
#                 "url": new_file_path,
#             }
#         else:
#             # Upload new file and create record
#             new_file_path = upload_file_to_s3(file, name)
#             new_file_record = GrammerFiles(name=name, root_word_id=root_word_id, file=new_file_path)
#             db.add(new_file_record)
#             db.commit()

#             return {
#                 "id": new_file_record.id,
#                 "name": name,
#                 "root_word_id": root_word_id,
#                 "file": new_file_path,
#                 "url": new_file_path
#             }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# # Generate URL for accessing a file
# def generate_file_url(file_name: str) -> str:
#     return f"{AWS_URL}/{file_name}"

# # Route for retrieving a file by root_word_id
# @file_management_router.get("/get-file", summary="Get File")
# async def get_file(root_word_id: int, db: Session = Depends(get_db)):
#     try:
#         existing_file = db.query(GrammerFiles).filter(GrammerFiles.root_word_id == root_word_id).first()
#         if not existing_file:
#             raise HTTPException(status_code=404, detail="File not found")

#         file_url = generate_file_url(existing_file.file)
#         return {
#             "success": True,
#             "message": "File retrieved successfully",
#             "data": file_url
#         }
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# # Route for deleting a file by root_word_id
# @file_management_router.delete("/delete-file", summary="Delete File")
# async def delete_file(root_word_id: int, db: Session = Depends(get_db)):
#     try:
#         existing_file = db.query(GrammerFiles).filter(GrammerFiles.root_word_id == root_word_id).first()
#         if not existing_file:
#             raise HTTPException(status_code=404, detail="File not found")

#         # Delete file from S3
#         s3 = get_s3_client()
#         s3.delete_object(Bucket=BUCKET_NAME, Key=existing_file.file)

#         # Delete record from database
#         db.delete(existing_file)
#         db.commit()

#         return {
#             "success": True,
#             "message": "File deleted successfully"
#         }
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
