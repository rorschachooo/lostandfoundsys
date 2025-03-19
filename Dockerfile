# Use Debian-based Node image as base (for frontend build)
FROM node:16 as frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy frontend package.json files
COPY front/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY front/ ./

# Build frontend project
RUN npm run build

# Use Python 3.7.9 image as base (for backend)
FROM python:3.7.9

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements.txt
COPY admin/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY admin/ ./

# Copy build artifacts from frontend build stage
COPY --from=frontend-build /app/frontend/dist ./static/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Django application port
EXPOSE 8000

# Startup command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]