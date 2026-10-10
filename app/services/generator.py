
import re
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import STORAGE_DIR
from app.models import Certificate, Job
from app.services.pdf import make_certificate_pdf


def validate_recipient(name: str, email: str) -> str | None:
    """Return an error message if the recipient is invalid."""
    if not name.strip():
        return "name is required"

    if len(name) > 100:
        return "name too long (max 100)"

    email = email.strip()
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(email_pattern, email):
        return "invalid email"

    return None


def process_job(db: Session, job: Job, recipients: list) -> None:
    """Generate each recipient's PDF and record individual outcomes."""
    storage_root = Path(STORAGE_DIR)

    try:
        for index, recipient in enumerate(recipients, start=1):
            certificate = Certificate(
                job_id=job.id,
                index=index,
                recipient_name=recipient.name,
                recipient_email=recipient.email,
                status="PENDING",
            )
            db.add(certificate)
            db.flush()

            try:
                error = validate_recipient(recipient.name, recipient.email)

                if error:
                    certificate.status = "FAILED"
                    certificate.error_message = error
                else:
                    output_path = (
                        storage_root / str(job.id) / f"{certificate.id}.pdf"
                    )
                    make_certificate_pdf(
                        recipient_name=recipient.name.strip(),
                        course_name=job.course_name,
                        issue_date=job.issue_date,
                        output_path=str(output_path),
                    )
                    certificate.status = "SUCCESS"
                    certificate.file_path = str(output_path)

            except Exception:
                certificate.status = "FAILED"
                certificate.error_message = "PDF generation failed"

            db.flush()

        db.refresh(job)
        certificates = (
            db.query(Certificate)
            .filter(Certificate.job_id == job.id)
            .all()
        )

        job.total = len(certificates)
        job.succeeded = sum(c.status == "SUCCESS" for c in certificates)
        job.failed = sum(c.status == "FAILED" for c in certificates)

        if job.succeeded == job.total:
            job.status = "COMPLETED"
        elif job.failed == job.total:
            job.status = "FAILED"
        else:
            job.status = "COMPLETED_WITH_ERRORS"

        job.completed_at = datetime.now(timezone.utc)
        db.commit()

    except Exception:
        db.rollback()
        raise
