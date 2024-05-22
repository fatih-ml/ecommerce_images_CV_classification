# Stage 1: Build
FROM python:3.11-slim AS build

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies
RUN apt-get remove -y build-essential && apt-get autoremove -y && apt-get clean

# Copy the application code
COPY . .

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /app /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
