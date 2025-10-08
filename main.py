from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from database import get_db

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Therapy Management API",
    description="API for managing therapists and patients with assignment capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
# Usage: GET / - Returns a welcome message to verify the API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to Therapy Management API"}

# Therapist endpoints
# Usage: POST /therapists/ - Creates a new therapist with validation for unique license number and email
# Request body: {"name": "string", "license_number": "string", "email": "string", "specialization": "string"}
# Returns: Created therapist object with generated ID
@app.post("/therapists/", response_model=schemas.Therapist)
def create_therapist(therapist: schemas.TherapistCreate, db: Session = Depends(get_db)):
    # Check if license number already exists
    existing_therapist = db.query(models.Therapist).filter(
        models.Therapist.license_number == therapist.license_number
    ).first()
    if existing_therapist:
        raise HTTPException(status_code=400, detail="License number already exists")
    
    # Check if email already exists
    existing_email = db.query(models.Therapist).filter(
        models.Therapist.email == therapist.email
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    db_therapist = models.Therapist(**therapist.dict())
    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

# Usage: GET /therapists/ - Retrieves a paginated list of all therapists
# Query parameters: skip (offset, default=0), limit (max records, default=100)
# Returns: List of therapist objects
@app.get("/therapists/", response_model=List[schemas.Therapist])
def get_therapists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    therapists = db.query(models.Therapist).filter(models.Therapist.last_name.like('%kubas%')).offset(skip).limit(limit).all()
    return therapists

# Usage: GET /therapists/{therapist_id} - Retrieves a specific therapist by ID with their assigned patients
# Path parameter: therapist_id (integer)
# Returns: Therapist object including list of assigned patients
@app.get("/therapists/{therapist_id}", response_model=schemas.TherapistWithPatients)
def get_therapist(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

# Usage: GET /therapists/{therapist_id}/patients - Retrieves all patients assigned to a specific therapist
# Path parameter: therapist_id (integer)
# Returns: List of patient objects assigned to the therapist
@app.get("/therapists/{therapist_id}/patients", response_model=List[schemas.Patient])
def get_therapist_patients(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist.patients

# Patient endpoints
# Usage: POST /patients/ - Creates a new patient with optional therapist assignment
# Request body: {"name": "string", "email": "string", "phone": "string", "therapist_id": int (optional)}
# Returns: Created patient object with generated ID
@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_patient = db.query(models.Patient).filter(
        models.Patient.email == patient.email
    ).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # If therapist_id is provided, verify it exists
    if patient.therapist_id:
        therapist = db.query(models.Therapist).filter(
            models.Therapist.id == patient.therapist_id
        ).first()
        if not therapist:
            raise HTTPException(status_code=404, detail="Therapist not found")
    
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Usage: GET /patients/ - Retrieves a paginated list of all patients
# Query parameters: skip (offset, default=0), limit (max records, default=100)
# Returns: List of patient objects
@app.get("/patients/", response_model=List[schemas.Patient])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

# Usage: GET /patients/{patient_id} - Retrieves a specific patient by ID with their assigned therapist
# Path parameter: patient_id (integer)
# Returns: Patient object including assigned therapist information (if any)
@app.get("/patients/{patient_id}", response_model=schemas.PatientWithTherapist)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Usage: PUT /patients/{patient_id}/assign-therapist/{therapist_id} - Assigns a therapist to a patient
# Path parameters: patient_id (integer), therapist_id (integer)
# Returns: Updated patient object with assigned therapist
@app.put("/patients/{patient_id}/assign-therapist/{therapist_id}", response_model=schemas.Patient)
def assign_therapist_to_patient(patient_id: int, therapist_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    
    patient.therapist_id = therapist_id
    db.commit()
    db.refresh(patient)
    return patient

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)