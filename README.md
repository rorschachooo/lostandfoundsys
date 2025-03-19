# Lost and Found Management System

A comprehensive lost and found management system built with Django (backend) and Vue.js (frontend).

## Project Structure

- `admin/`: Django backend for the system
- `front/`: Vue.js frontend application
- `db_lostfoundmgr_sys.sql`: Database schema and initial data

## Backend Setup

1. Navigate to the admin directory:
   ```
   cd admin
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database using the provided SQL file

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Frontend Setup

1. Navigate to the front directory:
   ```
   cd front
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

## Features

- Lost item registration and management
- Found item registration and management
- User authentication and authorization
- Admin dashboard for system management 