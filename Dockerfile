FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the web application uses
EXPOSE 8080

# Run the command to start the service when the container launches
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
