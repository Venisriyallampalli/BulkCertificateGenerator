
def test_rejects_empty_recipients(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": [],
        },
    )

    assert response.status_code == 422


def test_rejects_more_than_200_recipients(client):
    recipients = [
        {"name": f"Student {i}", "email": f"student{i}@example.com"}
        for i in range(201)
    ]

    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "2026-10-08",
            "recipients": recipients,
        },
    )

    assert response.status_code == 422


def test_rejects_invalid_issue_date(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Fundamentals",
            "issue_date": "not-a-date",
            "recipients": [
                {"name": "Asha Rao", "email": "asha@example.com"}
            ],
        },
    )

    assert response.status_code == 422


def test_rejects_course_name_over_150_characters(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "C" * 151,
            "issue_date": "2026-10-08",
            "recipients": [
                {"name": "Asha Rao", "email": "asha@example.com"}
            ],
        },
    )

    assert response.status_code == 422
