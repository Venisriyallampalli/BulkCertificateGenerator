
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class RecipientInput(BaseModel):
    name: str
    email: str


class CreateJobRequest(BaseModel):
    course_name: str = Field(max_length=150)
    issue_date: date
    recipients: list[RecipientInput] = Field(min_length=1, max_length=200)


class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    index: int
    recipient_name: str
    recipient_email: str
    status: str
    error_message: str | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_name: str
    issue_date: date
    status: str
    total: int
    succeeded: int
    failed: int
    created_at: datetime
    completed_at: datetime | None = None
