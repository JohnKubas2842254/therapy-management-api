# therapy-management-api
Restore Skills Interview
A FastAPI-based REST API for managing therapists and patients with assignment capabilities.

## Features

- **Therapist Management**: Create and retrieve therapist information
- **Patient Management**: Create and retrieve patient information  
- **Assignment System**: Assign therapists to patients
- **Relationship Queries**: Get all patients for a specific therapist
- **PostgreSQL Database**: Persistent data storage with SQLAlchemy ORM
- **Docker Support**: Easy local development setup
- **Swagger UI**: Interactive API documentation
- **Data Validation**: Pydantic models for request/response validation

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
```bash
git clone <repository-url>
cd therapy-management-api
```

2. **Start the application:**
```bash
docker-compose up --build
```

3. **Access the API:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Manual Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL database and update DATABASE_URL in database.py**

3. **Run the application:**
```bash
uvicorn main:app --reload
```

## API Endpoints

### Therapists

- `POST /therapists/` - Create a new therapist
- `GET /therapists/` - Get all therapists
- `GET /therapists/{therapist_id}` - Get specific therapist
- `GET /therapists/{therapist_id}/patients` - Get all patients for a therapist

### Patients

- `POST /patients/` - Create a new patient
- `GET /patients/` - Get all patients
- `GET /patients/{patient_id}` - Get specific patient
- `PUT /patients/{patient_id}/assign-therapist/{therapist_id}` - Assign therapist to patient

## Example Usage

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Use the interactive interface to test endpoints

### Using curl

**Create a therapist:**
```bash
curl -X POST "http://localhost:8000/therapists/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Dr. Jane",
       "last_name": "Smith",
       "email": "jane.smith@example.com",
       "specialty": "Cognitive Behavioral Therapy",
       "license_number": "LIC123456",
       "phone": "+1-555-0123"
     }'
```

**Create a patient:**
```bash
curl -X POST "http://localhost:8000/patients/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com",
       "phone": "+1-555-0124",
       "date_of_birth": "1990-01-15",
       "emergency_contact": "Jane Doe: +1-555-0125"
     }'
```

**Assign therapist to patient:**
```bash
curl -X PUT "http://localhost:8000/patients/1/assign-therapist/1"
```

**Get all patients for a therapist:**
```bash
curl "http://localhost:8000/therapists/1/patients"
```

## Database Schema

### Therapists Table
- `id` (Primary Key)
- `first_name`
- `last_name` 
- `email` (Unique)
- `specialty`
- `license_number` (Unique)
- `phone`
- `created_at`

### Patients Table
- `id` (Primary Key)
- `first_name`
- `last_name`
- `email` (Unique)
- `phone`
- `date_of_birth`
- `emergency_contact`
- `therapist_id` (Foreign Key, Optional)
- `created_at`

## Project Structure

```
therapy-management-api/
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── database.py          # Database configuration and connection
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Multi-container Docker setup
└── README.md           # This file
```

## Key Concepts for Interview

1. **FastAPI**: Modern Python web framework with automatic API documentation
2. **SQLAlchemy ORM**: Object-Relational Mapping for database interactions
3. **Pydantic**: Data validation and serialization using Python type hints
4. **PostgreSQL**: Relational database for data persistence
5. **Docker**: Containerization for consistent development environments
6. **REST API**: RESTful endpoint design following HTTP conventions
7. **Foreign Keys**: Database relationships between therapists and patients

## Troubleshooting

**Database connection issues:**
- Ensure PostgreSQL is running: `docker-compose logs db`
- Check connection string in `database.py`

**Port conflicts:**
- Change ports in `docker-compose.yml` if 8000 or 5432 are in use

**Module import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Next Steps / Enhancements

- Add authentication and authorization
- Implement appointment scheduling
- Add patient medical records
- Create audit logs for data changes
- Add email notifications
- Implement soft deletes
- Add API rate limiting