
from datetime import date
from pathlib import Path

from app.services.pdf import make_certificate_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "scratch"

issue_date = date(2026, 10, 8)
course_name = "Python Fundamentals"

test_recipients = [
    "Asha Rao",
    "A Very Long Recipient Name Designed to Test Whether the Certificate Layout Handles Ninety Characters Without Overflowing the Page",
    "Zoë Müller",
]

for index, recipient_name in enumerate(test_recipients, start=1):
    output_path = OUTPUT_DIR / f"test_certificate_{index}.pdf"

    generated_path = make_certificate_pdf(
        recipient_name=recipient_name,
        course_name=course_name,
        issue_date=issue_date,
        output_path=str(output_path),
    )

    print(f"Generated: {generated_path}")
