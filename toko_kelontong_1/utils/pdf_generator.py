from fpdf import FPDF
from config import get_db_connection

def generate_pdf_struk():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT p.id, s.nama, p.jumlah, s.harga, p.tanggal FROM pemesanan p JOIN stok s ON p.id_barang = s.id")
    data = cursor.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Struk Pemesanan Barang", ln=True, align='C')
    pdf.ln()

    for row in data:
        pdf.cell(200, 10, txt=f"{row['tanggal']} - {row['nama']} x{row['jumlah']} = Rp{row['jumlah']*row['harga']}", ln=True)
    
    pdf.output("static/struk_pesanan.pdf")

def generate_pdf_laporan():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stok")
    data = cursor.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Laporan Stok Barang", ln=True, align='C')
    pdf.ln()

    for row in data:
        pdf.cell(200, 10, txt=f"{row['nama']} - Stok: {row['stok']} - Harga: Rp{row['harga']}", ln=True)
    
    pdf.output("static/laporan_stok.pdf")
