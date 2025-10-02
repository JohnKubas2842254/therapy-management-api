from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Base schemas
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: str
    emergency_contact: str

class TherapistBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    specialty: str
    license_number: str
    phone: str

# Create schemas (for input)
class PatientCreate(PatientBase):
    therapist_id: Optional[int] = None

class TherapistCreate(TherapistBase):
    pass

# Response schemas (for output) - without circular references
class Patient(PatientBase):
    id: int
    therapist_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Therapist(TherapistBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Extended schemas with relationships (use carefully)
class TherapistWithPatients(Therapist):
    patients: List[Patient] = []

class PatientWithTherapist(Patient):
    therapist: Optional[Therapist] = None