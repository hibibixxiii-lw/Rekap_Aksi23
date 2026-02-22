from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import fonts
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from database import get_all_data, get_total_debit

def export_to_pdf(filepath, tahun, stasi):
    doc = SimpleDocTemplate(filepath)
    elements = []

    style = ParagraphStyle(name='Normal', fontSize=12)

    elements.append(Paragraph("REKAP AKSI", style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Tahun: {tahun}", style))
    elements.append(Paragraph(f"Stasi/Kring: {stasi}", style))
    elements.append(Spacer(1, 0.3 * inch))

    data = [["No", "Nama", "Debit", "Jumlah Sementara"]]

    db_data = get_all_data()
    running_total = 0

    for i, row in enumerate(db_data, start=1):
        running_total += row[2]
        data.append([i, row[1], row[2], running_total])

    data.append(["", "Total Debit", get_total_debit(), ""])

    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])

    elements.append(table)
    doc.build(elements)
