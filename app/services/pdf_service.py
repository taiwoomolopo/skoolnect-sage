from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(text, filename="lesson.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 15

    c.save()
    return filename