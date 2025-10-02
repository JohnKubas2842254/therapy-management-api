from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Therapist(Base):
    __tablename__ = "therapists"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    specialty = Column(String)
    license_number = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to patients
    patients = relationship("Patient", back_populates="therapist")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(String)
    emergency_contact = Column(String)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to therapist
    therapist = relationship("Therapist", back_populates="patients")