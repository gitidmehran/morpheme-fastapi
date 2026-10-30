# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file for app_one into the container
COPY app_one/requirements.txt .

# Install dependencies for app_one
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app_one source code into the container
COPY app_one/ .

# Expose port 8001 for app_one
EXPOSE 8001

# Run the FastAPI application for app_one
CMD ["uvicorn", "morpheme_app.main:routers", "--host", "0.0.0.0", "--port", "8001", "--reload"]
