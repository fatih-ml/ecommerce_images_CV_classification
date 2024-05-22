# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Define environment variable to ensure Python outputs everything to the terminal without buffering it.
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
