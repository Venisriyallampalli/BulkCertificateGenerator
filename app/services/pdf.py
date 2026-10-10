from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FONT_PATH = PROJECT_ROOT / "assets" / "fonts" / "DejaVuSans.ttf"
FONT_NAME = "CertificateSans"

NAVY = colors.HexColor("#102B46")
GOLD = colors.HexColor("#B79550")
PALE_GOLD = colors.HexColor("#D8C28E")
INK = colors.HexColor("#24384A")
PAPER = colors.HexColor("#FFFEFA")


def register_font() -> None:
    """Register the bundled Unicode font once."""
    if not FONT_PATH.is_file():
        raise FileNotFoundError(
            f"DejaVu Sans font not found at {FONT_PATH}. "
            "Ensure assets/fonts/DejaVuSans.ttf exists."
        )
    if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))


def _fit_size(text: str, max_width: float, starting_size: float,
              minimum_size: float = 8) -> float:
    """Reduce the font size until text fits the available width."""
    size = starting_size
    while size > minimum_size and pdfmetrics.stringWidth(text, FONT_NAME, size) > max_width:
        size = max(minimum_size, size - 0.5)
    return size


def _centered(pdf: canvas.Canvas, text: str, x: float, y: float,
              size: float, color: colors.Color, max_width: float,
              minimum_size: float = 8) -> None:
    text = str(text)
    size = _fit_size(text, max_width, size, minimum_size)
    pdf.setFillColor(color)
    pdf.setFont(FONT_NAME, size)
    pdf.drawCentredString(x, y, text)


def _leaf(pdf: canvas.Canvas, x: float, y: float, angle: float,
          scale: float = 1.0) -> None:
    """Draw a single laurel leaf."""
    pdf.saveState()
    pdf.translate(x, y)
    pdf.rotate(angle)
    pdf.setFillColor(GOLD)
    path = pdf.beginPath()
    path.moveTo(0, 0)
    path.curveTo(4 * scale, 2 * scale, 8 * scale, 8 * scale, 1 * scale, 12 * scale)
    path.curveTo(-3 * scale, 8 * scale, -3 * scale, 3 * scale, 0, 0)
    path.close()
    pdf.drawPath(path, fill=1, stroke=0)
    pdf.restoreState()


def _laurel(pdf: canvas.Canvas, base_x: float, base_y: float, side: int) -> None:
    """Draw a slim gold laurel branch in the left or right margin."""
    points = []
    for i in range(11):
        t = i / 10
        points.append((
            base_x + side * (5 + 17 * t - 3 * t * t),
            base_y + 8 + 190 * t,
        ))

    pdf.saveState()
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.2)
    path = pdf.beginPath()
    path.moveTo(points[0][0], points[0][1])
    for x, y in points[1:]:
        path.lineTo(x, y)
    pdf.drawPath(path, stroke=1, fill=0)

    for i, (x, y) in enumerate(points[1:-1], start=1):
        _leaf(pdf, x, y, (30 + i * 2) * side, 0.68)
        _leaf(pdf, x, y + 1, (145 + i * 2) * side, 0.64)
    pdf.restoreState()


def _graduation_cap(pdf: canvas.Canvas, cx: float, y: float) -> None:
    """Draw the graduation-cap icon above the title."""
    pdf.saveState()
    pdf.setFillColor(NAVY)
    path = pdf.beginPath()
    path.moveTo(cx - 25, y + 8)
    path.lineTo(cx, y + 20)
    path.lineTo(cx + 25, y + 8)
    path.lineTo(cx, y - 4)
    path.close()
    pdf.drawPath(path, fill=1, stroke=0)
    pdf.roundRect(cx - 16, y - 10, 32, 10, 2, fill=1, stroke=0)

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)
    pdf.line(cx + 22, y + 8, cx + 24, y - 8)
    pdf.setFillColor(GOLD)
    pdf.circle(cx + 24, y - 10, 1.8, fill=1, stroke=0)
    pdf.restoreState()


def _seal(pdf: canvas.Canvas, cx: float, cy: float) -> None:
    """Draw a compact gold seal in the gap between the footer columns."""
    pdf.saveState()
    pdf.setFillColor(GOLD)
    pdf.circle(cx, cy, 23, fill=1, stroke=0)
    pdf.setStrokeColor(PAPER)
    pdf.setLineWidth(1.2)
    pdf.circle(cx, cy, 18.5, fill=0, stroke=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.1)

    # Open-book icon.
    path = pdf.beginPath()
    path.moveTo(cx - 11, cy + 6)
    path.curveTo(cx - 6, cy + 8, cx - 2, cy + 4, cx, cy + 3)
    path.curveTo(cx + 3, cy + 5, cx + 7, cy + 8, cx + 11, cy + 6)
    path.lineTo(cx + 11, cy - 7)
    path.curveTo(cx + 6, cy - 5, cx + 3, cy - 6, cx, cy - 7)
    path.curveTo(cx - 3, cy - 6, cx - 7, cy - 5, cx - 11, cy - 7)
    path.close()
    pdf.drawPath(path, fill=0, stroke=1)
    pdf.line(cx, cy + 3, cx, cy - 7)
    pdf.restoreState()


def make_certificate_pdf(
    recipient_name: str,
    course_name: str,
    issue_date: date,
    output_path: str,
) -> str:
    """Generate a landscape A4 certificate matching the supplied PDF design."""
    register_font()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output.with_name(output.name + ".tmp")
    page_w, page_h = landscape(A4)
    cx = page_w / 2

    try:
        pdf = canvas.Canvas(str(temp_path), pagesize=(page_w, page_h), pageCompression=1)
        pdf.setTitle(f"Certificate of Completion - {recipient_name}")
        pdf.setAuthor("Bulk Certificate Generator")

        # Warm-white background and navy/gold frame.
        pdf.setFillColor(PAPER)
        pdf.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(5)
        pdf.rect(17, 17, page_w - 34, page_h - 34, fill=0, stroke=1)
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(1.4)
        pdf.rect(26, 26, page_w - 52, page_h - 52, fill=0, stroke=1)
        pdf.setStrokeColor(PALE_GOLD)
        pdf.setLineWidth(0.55)
        pdf.rect(32, 32, page_w - 64, page_h - 64, fill=0, stroke=1)

        # Navy triangular corner accents.
        corner = 43
        pdf.setFillColor(NAVY)
        for sx, sy in ((0, 0), (page_w, 0), (0, page_h), (page_w, page_h)):
            dx = corner if sx == 0 else -corner
            dy = corner if sy == 0 else -corner
            path = pdf.beginPath()
            path.moveTo(sx, sy)
            path.lineTo(sx + dx, sy)
            path.lineTo(sx, sy + dy)
            path.close()
            pdf.drawPath(path, fill=1, stroke=0)

        # Fine gold accents near the four edges.
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(1)
        pdf.line(31, page_h - 38, 104, page_h - 38)
        pdf.line(page_w - 104, page_h - 38, page_w - 31, page_h - 38)
        pdf.line(31, 38, 104, 38)
        pdf.line(page_w - 104, 38, page_w - 31, 38)

        # Side decoration and cap icon.
        _laurel(pdf, 47, 82, 1)
        _laurel(pdf, page_w - 47, 82, -1)
        _graduation_cap(pdf, cx, page_h - 67)

        _centered(pdf, "CERTIFICATE OF COMPLETION", cx, page_h - 126,
                  25, NAVY, page_w - 170, 17)
        _centered(pdf, "THIS CERTIFIES THAT", cx, page_h - 157,
                  9, GOLD, page_w - 200, 8)

        # Divider with a central diamond.
        divider_y = page_h - 178
        pdf.setStrokeColor(PALE_GOLD)
        pdf.setLineWidth(0.9)
        pdf.line(cx - 170, divider_y, cx - 8, divider_y)
        pdf.line(cx + 8, divider_y, cx + 170, divider_y)
        pdf.setFillColor(GOLD)
        path = pdf.beginPath()
        path.moveTo(cx, divider_y + 3.5)
        path.lineTo(cx + 3.5, divider_y)
        path.lineTo(cx, divider_y - 3.5)
        path.lineTo(cx - 3.5, divider_y)
        path.close()
        pdf.drawPath(path, fill=1, stroke=0)

        _centered(pdf, recipient_name, cx, page_h - 218,
                  22, NAVY, page_w - 190, 12)
        _centered(pdf, "has successfully completed the course", cx, page_h - 246,
                  11, INK, page_w - 190, 9)
        _centered(pdf, course_name, cx, page_h - 276,
                  16, NAVY, page_w - 200, 10)
        _centered(pdf, "in recognition of dedication and achievement", cx, page_h - 300,
                  9, INK, page_w - 200, 8)

        formatted_date = f"{issue_date.day} {issue_date.strftime('%B %Y')}"
        _centered(pdf, f"ISSUED ON  {formatted_date}", cx, page_h - 330,
                  9, GOLD, page_w - 190, 8)

        # Footer layout: two separate columns with the seal in the clear center gap.
        # The labels are centered under their own lines and cannot overlap the seal.
        footer_line_y = 66
        footer_label_y = 47
        left_center = cx - 150
        right_center = cx + 150
        line_half_width = 55

        pdf.setStrokeColor(INK)
        pdf.setLineWidth(0.7)
        pdf.line(left_center - line_half_width, footer_line_y,
                 left_center + line_half_width, footer_line_y)
        pdf.line(right_center - line_half_width, footer_line_y,
                 right_center + line_half_width, footer_line_y)

        _centered(pdf, "CERTIFICATE COORDINATOR", left_center, footer_label_y,
                  6.5, INK, 135, 6)
        _centered(pdf, "AUTHORIZED SIGNATURE", right_center, footer_label_y,
                  6.5, INK, 135, 6)
        _seal(pdf, cx, footer_line_y - 1)

        pdf.showPage()
        pdf.save()
        os.replace(str(temp_path), str(output))
        return str(output)

    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise
