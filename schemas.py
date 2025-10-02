from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Therapist schemas
class TherapistBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    specialty: str
    license_number: str
    phone: str

class TherapistCreate(TherapistBase):
    pass

class Therapist(TherapistBase):
    id: int
    created_at: datetime
    patients: List['Patient'] = []

    class Config:
        from_attributes = True

# Patient schemas
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: str
    emergency_contact: str

class PatientCreate(PatientBase):
    therapist_id: Optional[int] = None

class Patient(PatientBase):
    id: int
    therapist_id: Optional[int] = None
    created_at: datetime
    therapist: Optional[Therapist] = None

    class Config:
        from_attributes = True

# Forward reference resolution
Therapist.model_rebuild()