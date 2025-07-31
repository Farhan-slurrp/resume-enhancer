import fitz
from reportlab.pdfgen import canvas

def read_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "".join(page.get_text() for page in doc)

def write_pdf(text: str, output_path: str):
    c = canvas.Canvas(output_path)
    c.setFont("Helvetica", 12)

    y = 800
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15

    c.save()