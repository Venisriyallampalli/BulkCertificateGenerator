
def test_create_job_success(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Asha Rao",
                    "email": "asha@example.com",
                },
                {
                    "name": "Rahul Kumar",
                    "email": "rahul@example.com",
                },
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["course_name"] == "Python Fundamentals"
    assert data["total"] == 2
    assert data["succeeded"] == 2
    assert data["failed"] == 0
    assert data["status"] == "COMPLETED"
