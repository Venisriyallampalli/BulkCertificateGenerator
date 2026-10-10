<<<<<<< HEAD
# Bulk Certificate Generator

A Python REST API that generates personalized PDF certificates for multiple recipients in a single request. The application validates recipient details independently, records each certificate's status, and allows successful PDFs to be downloaded.

## Features

- Generate certificates for up to 200 recipients per job.
- Validate course details, issue dates, recipient names, and email addresses.
- Generate personalized PDF certificates using ReportLab and DejaVu Sans.
- Continue processing when an individual recipient fails validation or PDF generation.
- Track job totals, successful certificates, and failed certificates.
- Retrieve job summaries and filter certificate records by status.
- Download successfully generated certificates.
- Store job and certificate records in SQLite.

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- pytest
- FastAPI TestClient

## Project Structure

```text
certificate-generator/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── jobs.py
│   │   └── certificates.py
│   └── services/
│       ├── generator.py
│       └── pdf.py
├── assets/
│   └── fonts/
│       └── DejaVuSans.ttf
├── storage/
├── tests/
│   ├── conftest.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_generation.py
│   ├── test_failures.py
│   └── test_retrieval.py
├── requirements.txt
├── README.md
├── DESIGN.md
└── .gitignore
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Verify the font

Ensure `DejaVuSans.ttf` exists at:

```text
assets/fonts/DejaVuSans.ttf
```

### 4. Start the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs` | Create and process a certificate job |
| GET | `/jobs/{job_id}` | Retrieve a job summary |
| GET | `/jobs/{job_id}/certificates` | Retrieve certificate records |
| GET | `/certificates/{certificate_id}/download` | Download a successful PDF |

### Create a job

Example request:

```json
{
  "course_name": "Python Fundamentals",
  "issue_date": "2026-10-08",
  "recipients": [
    {
      "name": "Asha Rao",
      "email": "asha@example.com"
    },
    {
      "name": "Rahul Kumar",
      "email": "rahul@example.com"
    }
  ]
}
```

The issue date must use ISO format (`YYYY-MM-DD`). A job can contain between 1 and 200 recipients.

### Filter certificate records

Retrieve all certificates:

```text
GET /jobs/1/certificates
```

Retrieve successful certificates:

```text
GET /jobs/1/certificates?status=SUCCESS
```

Retrieve failed certificates:

```text
GET /jobs/1/certificates?status=FAILED
```

### Download a certificate

```text
GET /certificates/{certificate_id}/download
```

Only successfully generated certificates with an available PDF can be downloaded.

## Job Statuses

- `COMPLETED`: All certificates were generated successfully.
- `FAILED`: All recipients failed processing.
- `COMPLETED_WITH_ERRORS`: Some certificates succeeded and others failed.

Each certificate has its own status and error message when processing fails.

## Run Tests

Activate the virtual environment and run:

```powershell
python -m pytest -v
```

The current automated test suite contains 14 tests, all passing.

## Design Notes

- SQLite stores job and certificate metadata.
- SQLAlchemy manages database access.
- Pydantic validates incoming request structure.
- Recipient-level validation allows a job to continue after an individual recipient fails.
- ReportLab generates the PDF documents.
- Integer-based certificate IDs are used in PDF filenames.
- Processing is synchronous: the job finishes before the creation request returns.
- Generated PDFs are stored under the configured storage directory.

See `DESIGN.md` for the detailed design specification.
=======
# Bulk Certificate Generator

A Python REST API that generates personalized PDF certificates for multiple recipients in a single request. The application validates recipient details independently, records each certificate's status, and allows successful PDFs to be downloaded.

## Features

- Generate certificates for up to 200 recipients per job.
- Validate course details, issue dates, recipient names, and email addresses.
- Generate personalized PDF certificates using ReportLab and DejaVu Sans.
- Continue processing when an individual recipient fails validation or PDF generation.
- Track job totals, successful certificates, and failed certificates.
- Retrieve job summaries and filter certificate records by status.
- Download successfully generated certificates.
- Store job and certificate records in SQLite.

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- pytest
- FastAPI TestClient

## Project Structure

```text
certificate-generator/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── jobs.py
│   │   └── certificates.py
│   └── services/
│       ├── generator.py
│       └── pdf.py
├── assets/
│   └── fonts/
│       └── DejaVuSans.ttf
├── storage/
├── tests/
│   ├── conftest.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   ├── test_generation.py
│   ├── test_failures.py
│   └── test_retrieval.py
├── requirements.txt
├── README.md
├── DESIGN.md
└── .gitignore
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Verify the font

Ensure `DejaVuSans.ttf` exists at:

```text
assets/fonts/DejaVuSans.ttf
```

### 4. Start the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs` | Create and process a certificate job |
| GET | `/jobs/{job_id}` | Retrieve a job summary |
| GET | `/jobs/{job_id}/certificates` | Retrieve certificate records |
| GET | `/certificates/{certificate_id}/download` | Download a successful PDF |

### Create a job

Example request:

```json
{
  "course_name": "Python Fundamentals",
  "issue_date": "2026-10-08",
  "recipients": [
    {
      "name": "Asha Rao",
      "email": "asha@example.com"
    },
    {
      "name": "Rahul Kumar",
      "email": "rahul@example.com"
    }
  ]
}
```

The issue date must use ISO format (`YYYY-MM-DD`). A job can contain between 1 and 200 recipients.

### Filter certificate records

Retrieve all certificates:

```text
GET /jobs/1/certificates
```

Retrieve successful certificates:

```text
GET /jobs/1/certificates?status=SUCCESS
```

Retrieve failed certificates:

```text
GET /jobs/1/certificates?status=FAILED
```

### Download a certificate

```text
GET /certificates/{certificate_id}/download
```

Only successfully generated certificates with an available PDF can be downloaded.

## Job Statuses

- `COMPLETED`: All certificates were generated successfully.
- `FAILED`: All recipients failed processing.
- `COMPLETED_WITH_ERRORS`: Some certificates succeeded and others failed.

Each certificate has its own status and error message when processing fails.

## Run Tests

Activate the virtual environment and run:

```powershell
python -m pytest -v
```

The current automated test suite contains 14 tests, all passing.

## Design Notes

- SQLite stores job and certificate metadata.
- SQLAlchemy manages database access.
- Pydantic validates incoming request structure.
- Recipient-level validation allows a job to continue after an individual recipient fails.
- ReportLab generates the PDF documents.
- Integer-based certificate IDs are used in PDF filenames.
- Processing is synchronous: the job finishes before the creation request returns.
- Generated PDFs are stored under the configured storage directory.

See `DESIGN.md` for the detailed design specification.
>>>>>>> e6800a40c33f334fdb367423cde6c908586ffc0f
