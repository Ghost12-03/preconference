# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Expose port 8080 for Cloud Run
EXPOSE 8000

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "deploy:app"]
