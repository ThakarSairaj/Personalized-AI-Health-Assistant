from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import date


def generate_medical_report_pdf(user, report):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    LEFT = 1 * inch
    RIGHT = width - 1 * inch
    TOP = height - 1 * inch
    BOTTOM = 1 * inch

    y = TOP

    styles = getSampleStyleSheet()
    body = styles["Normal"]
    body.fontSize = 10
    body.leading = 14

    heading_color = HexColor("#2F4F6F")

    # ================= HEADER (FIXED / ONCE) =================
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(heading_color)
    c.drawCentredString(width / 2, y, "MEDICAL REPORT")
    y -= 24

    c.setFont("Helvetica", 10)
    c.setFillColor(black)

    age = "-"
    if user.dob:
        today = date.today()
        age = today.year - user.dob.year - (
            (today.month, today.day) < (user.dob.month, user.dob.day)
        )

    # Patient info block (compact, one time)
    c.drawString(LEFT, y, f"Patient: {user.first_name} {user.last_name}")
    c.drawString(LEFT + 3.5 * inch, y, f"Gender: {user.gender}")
    y -= 14

    c.drawString(LEFT, y, f"Age: {age}")
    c.drawString(
        LEFT + 3.5 * inch,
        y,
        f"Reported On: {report.reported_at.strftime('%d-%m-%Y')}",
    )
    y -= 20

    # Single divider (only once in whole document)
    c.setLineWidth(1)
    c.line(LEFT, y, RIGHT, y)
    y -= 30

    # ================= MEDICAL CONTENT =================
    # Chief Complaint (start of narrative)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(heading_color)
    c.drawString(LEFT, y, "Chief Complaint")
    y -= 16

    complaint = Paragraph(report.chief_complaint or "-", body)
    w, h = complaint.wrap(RIGHT - LEFT, y)
    complaint.drawOn(c, LEFT, y - h)
    y -= h + 20

    # Clinical Details (continuation — no divider)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(LEFT, y, "Clinical Details")
    y -= 16

    details = [
        ("Symptoms", report.symptoms),
        ("Duration", report.duration),
        ("Onset Type", report.onset_type),
        ("Progression", report.progression),
        ("Severity", report.severity),
    ]

    for label, value in details:
        if value:
            p = Paragraph(f"<b>{label}:</b> {value}", body)
            w, h = p.wrap(RIGHT - LEFT, y)
            p.drawOn(c, LEFT, y - h)
            y -= h + 10

    # ================= FOOTER =================
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#555555"))

    disclaimer = Paragraph(
        "Disclaimer: This report is generated based on patient-reported information "
        "and is not a medical diagnosis. Please consult a qualified healthcare professional.",
        styles["Normal"],
    )

    w, h = disclaimer.wrap(RIGHT - LEFT, BOTTOM)
    disclaimer.drawOn(c, LEFT, BOTTOM - h)

    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer
