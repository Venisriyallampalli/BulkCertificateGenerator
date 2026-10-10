
def test_invalid_recipient_does_not_stop_other_certificates(client):
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

    job = response.json()
    assert job["total"] == 3
    assert job["succeeded"] == 2
    assert job["failed"] == 1
    assert job["status"] == "COMPLETED_WITH_ERRORS"

    certificates = client.get(
        f"/jobs/{job['id']}/certificates"
    ).json()

    assert len(certificates) == 3

    failed = [c for c in certificates if c["status"] == "FAILED"]
    successful = [c for c in certificates if c["status"] == "SUCCESS"]

    assert len(failed) == 1
    assert failed[0]["error_message"] == "name is required"
    assert len(successful) == 2


def test_all_invalid_recipients_make_job_failed(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "", "email": "asha@example.com"},
                {"name": "Rahul Kumar", "email": "invalid-email"},
            ],
        },
    )

    assert response.status_code == 201

    job = response.json()
    assert job["total"] == 2
    assert job["succeeded"] == 0
    assert job["failed"] == 2
    assert job["status"] == "FAILED"
