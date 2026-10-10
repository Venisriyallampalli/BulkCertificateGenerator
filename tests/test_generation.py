
from pathlib import Path

from pypdf import PdfReader


def test_generates_pdf_for_each_valid_recipient(client, tmp_path):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "Asha Rao", "email": "asha@example.com"},
                {"name": "Rahul Kumar", "email": "rahul@example.com"},
            ],
        },
    )

    assert response.status_code == 201
    job = response.json()

    assert job["succeeded"] == 2
    assert job["failed"] == 0

    certificates_response = client.get(
        f"/jobs/{job['id']}/certificates"
    )
    assert certificates_response.status_code == 200

    certificates = certificates_response.json()
    assert len(certificates) == 2

    for certificate in certificates:
        assert certificate["status"] == "SUCCESS"


def test_generated_pdf_is_readable(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "Zoë Müller", "email": "zoe@example.com"}
            ],
        },
    )

    assert response.status_code == 201
    job_id = response.json()["id"]

    certificates = client.get(
        f"/jobs/{job_id}/certificates?status=SUCCESS"
    ).json()

    assert len(certificates) == 1

    download = client.get(
        f"/certificates/{certificates[0]['id']}/download"
    )

    assert download.status_code == 200
    assert download.headers["content-type"] == "application/pdf"
    assert download.content.startswith(b"%PDF")
