from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    dob: date | None = None
    alias: str | None = None
    phone: str | None = None
    address: str | None = None
    notes: str | None = None
    case_number: str | None = None
    intel_number: str | None = None
    restricted_ssn: str | None = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    dob: date | None = None
    alias: str | None = None
    phone: str | None = None
    address: str | None = None
    notes: str | None = None
    case_number: str | None = None
    intel_number: str | None = None
    restricted_ssn: str | None = None


class SubjectOut(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class EncounterCreate(BaseModel):
    location: str | None = None
    summary: str
    encountered_at: datetime


class EncounterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    officer_id: int
    location: str | None = None
    summary: str
    encountered_at: datetime
