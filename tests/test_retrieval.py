
def test_get_job_and_filter_certificates(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "Asha Rao", "email": "asha@example.com"},
                {"name": "", "email": "invalid-email"},
                {"name": "Rahul Kumar", "email": "rahul@example.com"},
            ],
        },
    )

    assert response.status_code == 201
    job_id = response.json()["id"]

    # Retrieve job summary
    job_response = client.get(f"/jobs/{job_id}")
    assert job_response.status_code == 200
    assert job_response.json()["status"] == "COMPLETED_WITH_ERRORS"

    # Retrieve all certificates
    all_response = client.get(f"/jobs/{job_id}/certificates")
    assert all_response.status_code == 200
    assert len(all_response.json()) == 3

    # Filter successful certificates
    success_response = client.get(
        f"/jobs/{job_id}/certificates?status=SUCCESS"
    )
    assert success_response.status_code == 200
    assert len(success_response.json()) == 2

    # Filter failed certificates
    failed_response = client.get(
        f"/jobs/{job_id}/certificates?status=FAILED"
    )
    assert failed_response.status_code == 200
    assert len(failed_response.json()) == 1


def test_get_nonexistent_job_returns_404(client):
    response = client.get("/jobs/999")
    assert response.status_code == 404


def test_get_certificates_for_nonexistent_job_returns_404(client):
    response = client.get("/jobs/999/certificates")
    assert response.status_code == 404


def test_download_failed_certificate_returns_404(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "", "email": "invalid-email"}
            ],
        },
    )

    assert response.status_code == 201
    job_id = response.json()["id"]

    certificates = client.get(
        f"/jobs/{job_id}/certificates"
    ).json()

    certificate_id = certificates[0]["id"]

    download_response = client.get(
        f"/certificates/{certificate_id}/download"
    )

    assert download_response.status_code == 404


def test_download_nonexistent_certificate_returns_404(client):
    response = client.get("/certificates/999/download")
    assert response.status_code == 404
