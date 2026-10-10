
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Certificate, Job
from app.schemas import (
    CertificateResponse,
    CreateJobRequest,
    JobResponse,
)
from app.services.generator import process_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    request: CreateJobRequest,
    db: Session = Depends(get_db),
):
    course_name = request.course_name.strip()

    if not course_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="course_name must not be blank",
        )

    job = Job(
        course_name=course_name,
        issue_date=request.issue_date,
        status="PENDING",
        total=len(request.recipients),
        succeeded=0,
        failed=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        process_job(db, job, request.recipients)
        db.refresh(job)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process certificate job",
        )

    return job


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.get(
    "/{job_id}/certificates",
    response_model=list[CertificateResponse],
)
def get_job_certificates(
    job_id: int,
    status_filter: str | None = Query(
        default=None,
        alias="status",
        pattern="^(SUCCESS|FAILED)$",
    ),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    query = db.query(Certificate).filter(
        Certificate.job_id == job_id
    )

    if status_filter is not None:
        query = query.filter(
            Certificate.status == status_filter
        )

    return query.order_by(Certificate.index).all()
