import os
import sys
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .routers.morphemes import morphemes_router
from .config.db_config import SessionLocal, get_db, engine
from .models.Morpheme_model import Base
# from .routers.file_management import file_management_router

# sys.path.append(os.path.join(os.path.dirname(__file__), 'morpheme_app'))
# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost",  # Frontend URL
    "http://localhost:3000",  # For React or other frontend running locally
    "http://49.13.21.18:8507",  #production domain
    "https://qgrmr-dev.researchquran.org",  #production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database initialization
Base.metadata.create_all(bind=engine)

# Include the Morphemes and File Management APIs
app.include_router(morphemes_router)
# app.include_router(file_management_router)

# Modify the root endpoint to check the DB connection
@app.get("/db")
def check_db_connection(db: SessionLocal = Depends(get_db)):
    try:
        # Execute a simple raw SQL query to test the connection
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"status": "Connection successful", "result": result}
        else:
            return {"status": "Unexpected result", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/")
def root():
    return {"Hello": "World"}


