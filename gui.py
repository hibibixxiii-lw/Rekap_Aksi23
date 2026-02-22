import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import insert_data, get_all_data, delete_last, delete_all, get_total_debit
from export_excel import export_to_excel
from export_pdf import export_to_pdf

def run_app():
    root = tk.Tk()
    root.title("Rekap Aksi v2.1")
    root.geometry("800x600")

    nama_var = tk.StringVar()
    debit_var = tk.StringVar()
    tahun_var = tk.StringVar()
    stasi_var = tk.StringVar()

    # ================= FUNCTIONS =================

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)

        data = get_all_data()
        running_total = 0

        for i, row in enumerate(data, start=1):
            running_total += row[2]
            tree.insert("", "end",
                        values=(i, row[1], row[2], running_total))

        total_debit = get_total_debit()
        total_label.config(text=f"Total Debit: Rp {total_debit}")
        keluarga_label.config(text=f"Total Keluarga: {len(data)}")

    def tambah_data():
        if not nama_var.get() or not debit_var.get():
            messagebox.showwarning("Peringatan", "Nama dan Debit wajib diisi!")
            return

        insert_data(nama_var.get(), int(debit_var.get()))
        nama_var.set("")
        debit_var.set("")
        refresh_table()

    def tambah_nominal(nominal):
        current = debit_var.get()
        if current == "":
            debit_var.set(str(nominal))
        else:
            debit_var.set(str(int(current) + nominal))

    def reset_debit():
        debit_var.set("")

    def undo_data():
        delete_last()
        refresh_table()

    def konfirmasi_hapus():
        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Export berhasil.\nKosongkan data sesi ini?"
        )
        if jawab:
            delete_all()
            refresh_table()

    def export_excel_file():
        if not tahun_var.get() or not stasi_var.get():
            messagebox.showwarning("Peringatan", "Isi Tahun dan Stasi!")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if filepath:
            export_to_excel(filepath, tahun_var.get(), stasi_var.get())
            konfirmasi_hapus()

    def export_pdf_file():
        if not tahun_var.get() or not stasi_var.get():
            messagebox.showwarning("Peringatan", "Isi Tahun dan Stasi!")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if filepath:
            export_to_pdf(filepath, tahun_var.get(), stasi_var.get())
            konfirmasi_hapus()

    # ================= LAYOUT =================

    frame_top = tk.Frame(root)
    frame_top.pack(pady=10)

    tk.Label(frame_top, text="Tahun:").grid(row=0, column=0)
    tk.Entry(frame_top, textvariable=tahun_var, width=10).grid(row=0, column=1)

    tk.Label(frame_top, text="Stasi/Kring:").grid(row=0, column=2)
    tk.Entry(frame_top, textvariable=stasi_var, width=20).grid(row=0, column=3)

    frame_input = tk.LabelFrame(root, text="Input Data")
    frame_input.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_input, text="Nama").grid(row=0, column=0)
    tk.Entry(frame_input, textvariable=nama_var, width=20).grid(row=0, column=1)

    tk.Label(frame_input, text="Debit").grid(row=0, column=2)
    tk.Entry(frame_input, textvariable=debit_var, width=15).grid(row=0, column=3)

    tk.Button(frame_input, text="Tambah", command=tambah_data).grid(row=0, column=4, padx=5)
    tk.Button(frame_input, text="Undo", command=undo_data).grid(row=0, column=5, padx=5)

    # ===== NOMINAL CEPAT =====
    frame_nominal = tk.LabelFrame(root, text="Nominal Cepat")
    frame_nominal.pack(fill="x", padx=10, pady=5)

    nominal_list = [1000, 2000, 5000, 10000, 20000, 50000, 100000]

    for i, nominal in enumerate(nominal_list):
        tk.Button(
            frame_nominal,
            text=f"Rp {nominal}",
            command=lambda n=nominal: tambah_nominal(n)
        ).grid(row=0, column=i, padx=5)

    tk.Button(frame_nominal, text="Reset", command=reset_debit).grid(row=0, column=7, padx=5)

    # ===== TABEL =====
    frame_table = tk.Frame(root)
    frame_table.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("No", "Nama", "Debit", "Jumlah Sementara")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    tree.heading("No", text="No")
    tree.column("No", width=40, anchor="center")

    tree.heading("Nama", text="Nama")
    tree.column("Nama", anchor="center")

    tree.heading("Debit", text="Debit")
    tree.column("Debit", anchor="center")

    tree.heading("Jumlah Sementara", text="Jumlah Sementara")
    tree.column("Jumlah Sementara", anchor="center")

    tree.pack(fill="both", expand=True)

    # ===== TOTAL =====
    frame_total = tk.Frame(root)
    frame_total.pack(fill="x", padx=10)

    keluarga_label = tk.Label(frame_total, text="Total Keluarga: 0")
    keluarga_label.pack(side="left", padx=10)

    total_label = tk.Label(frame_total, text="Total Debit: Rp 0")
    total_label.pack(side="left", padx=10)

    # ===== EXPORT =====
    frame_export = tk.Frame(root)
    frame_export.pack(pady=10)

    tk.Button(frame_export, text="Export Excel", command=export_excel_file).pack(side="left", padx=10)
    tk.Button(frame_export, text="Export PDF", command=export_pdf_file).pack(side="left", padx=10)

    refresh_table()
    root.mainloop()
