
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Certificate

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/{certificate_id}/download")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if certificate is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found",
        )

    if certificate.status != "SUCCESS" or not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate PDF is not available",
        )

    file_path = Path(certificate.file_path)

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Certificate PDF file not found",
        )

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf",
    )
