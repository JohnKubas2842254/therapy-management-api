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
@app.get("/")
def read_root():
    return {"message": "Welcome to Therapy Management API"}

# Therapist endpoints
@app.post("/therapists/", response_model=schemas.Therapist)
def create_therapist(therapist: schemas.TherapistCreate, db: Session = Depends(get_db)):
    db_therapist = models.Therapist(**therapist.dict())
    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

@app.get("/therapists/", response_model=List[schemas.Therapist])
def get_therapists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    therapists = db.query(models.Therapist).offset(skip).limit(limit).all()
    return therapists

@app.get("/therapists/{therapist_id}", response_model=schemas.Therapist)
def get_therapist(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

@app.get("/therapists/{therapist_id}/patients", response_model=List[schemas.Patient])
def get_therapist_patients(therapist_id: int, db: Session = Depends(get_db)):
    therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist.patients

# Patient endpoints
@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[schemas.Patient])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

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