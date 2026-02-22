from openpyxl import Workbook
from database import get_all_data, get_total_debit

def export_to_excel(filepath, tahun, stasi):
    wb = Workbook()
    ws = wb.active
    ws.title = "Rekap Aksi"

    # Header
    ws.append(["REKAP AKSI"])
    ws.append([f"Tahun: {tahun}"])
    ws.append([f"Stasi/Kring: {stasi}"])
    ws.append([])

    # Judul tabel
    ws.append(["No", "Nama", "Debit", "Jumlah Sementara"])

    data = get_all_data()
    running_total = 0

    for i, row in enumerate(data, start=1):
        running_total += row[2]
        ws.append([i, row[1], row[2], running_total])

    ws.append([])
    ws.append(["", "Total Debit", get_total_debit()])

    wb.save(filepath)
