from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import io
from io import BytesIO
from openpyxl import Workbook

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fungsi koneksi database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='toko_kelontong_2'
    )

# ======================== STOK BARANG ============================
@app.route('/')
@app.route('/stok', methods=['GET', 'POST'])
def stok():
    filter_nama = request.args.get('filter_nama', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if filter_nama:
            cursor.execute("SELECT * FROM barang WHERE nama LIKE %s", ('%' + filter_nama + '%',))
        else:
            cursor.execute("SELECT * FROM barang")
        data = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('stok.html', barang=data, filter_nama=filter_nama)

@app.route('/tambah_stok', methods=['POST'])
def tambah_stok():
    nama = request.form['nama']
    harga = request.form['harga']
    stok = request.form['stok']

    if not nama or not harga or not stok:
        flash('Semua field harus diisi.')
        return redirect(url_for('stok'))

    try:
        harga = float(harga)
        stok = int(stok)
    except ValueError:
        flash('Harga harus angka dan stok harus bilangan bulat.')
        return redirect(url_for('stok'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO barang (nama, harga, stok) VALUES (%s, %s, %s)", (nama, harga, stok))
        conn.commit()
        flash('Barang berhasil ditambahkan')
    except Exception as e:
        flash(f'Error saat menambahkan barang: {e}')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('stok'))

@app.route('/edit_stok/<int:id>', methods=['GET', 'POST'])
def edit_stok(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok_val = request.form['stok']

        if not nama or not harga or not stok_val:
            flash('Semua field harus diisi.')
            cursor.close()
            conn.close()
            return redirect(url_for('edit_stok', id=id))

        try:
            harga = float(harga)
            stok_val = int(stok_val)
        except ValueError:
            flash('Harga harus angka dan stok harus bilangan bulat.')
            cursor.close()
            conn.close()
            return redirect(url_for('edit_stok', id=id))

        try:
            cursor.execute("UPDATE barang SET nama=%s, harga=%s, stok=%s WHERE id=%s", (nama, harga, stok_val, id))
            conn.commit()
            flash('Data barang berhasil diperbarui')
        except Exception as e:
            flash(f'Error saat memperbarui data barang: {e}')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('stok'))

    try:
        cursor.execute("SELECT * FROM barang WHERE id=%s", (id,))
        data = cursor.fetchone()
        if not data:
            flash('Data barang tidak ditemukan.')
            return redirect(url_for('stok'))
    finally:
        cursor.close()
        conn.close()

    return render_template('edit_stok.html', barang=data)

@app.route('/hapus_stok/<int:id>')
def hapus_stok(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM barang WHERE id=%s", (id,))
        conn.commit()
        flash('Barang berhasil dihapus')
    except Exception as e:
        flash(f'Error saat menghapus barang: {e}')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('stok'))

# ======================== PEMESANAN ============================

@app.route('/pemesanan', methods=['GET', 'POST'])
def pemesanan():
    filter_nama = request.args.get('filter_nama', '')

    if request.method == 'POST':
        item_ids = request.form.getlist('barang_id')
        jumlahs = request.form.getlist('jumlah')

        if not item_ids or all(j == '' or j == '0' for j in jumlahs):
            flash('Pilih dan masukkan jumlah setidaknya satu barang.')
            return redirect(url_for('pemesanan'))

        total = 0
        detail_data = []

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            for i, barang_id in enumerate(item_ids):
                try:
                    jumlah = int(jumlahs[i])
                except ValueError:
                    flash('Jumlah harus berupa angka.')
                    raise

                if jumlah <= 0:
                    continue

                # Ambil data barang
                cursor.execute("SELECT * FROM barang WHERE id = %s", (barang_id,))
                barang = cursor.fetchone()
                cursor.fetchall()  # Buang sisa result set

                if not barang:
                    flash(f'Barang ID {barang_id} tidak ditemukan.')
                    raise Exception("Barang tidak ditemukan")

                if barang['stok'] < jumlah:
                    flash(f'Stok barang {barang["nama"]} tidak cukup.')
                    raise Exception("Stok tidak cukup")

                subtotal = barang['harga'] * jumlah
                total += subtotal
                detail_data.append((barang_id, jumlah, subtotal))

            if not detail_data:
                flash('Tidak ada barang valid dipesan.')
                raise Exception("Data kosong")

            # Simpan pesanan dan detail
            cursor.execute("INSERT INTO pesanan (total, tanggal) VALUES (%s, %s)", (total, datetime.now()))
            pesanan_id = cursor.lastrowid

            for barang_id, jumlah, subtotal in detail_data:
                cursor.execute("""
                    INSERT INTO detail_pesanan (pesanan_id, barang_id, jumlah, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (pesanan_id, barang_id, jumlah, subtotal))

                cursor.execute("UPDATE barang SET stok = stok - %s WHERE id = %s", (jumlah, barang_id))

            conn.commit()
            flash('Pesanan berhasil. Silakan cek preview struk berikut.')
            return redirect(url_for('preview_struk', pesanan_id=pesanan_id))


        except Exception as e:
            conn.rollback()
            print(f"Terjadi error saat menyimpan pesanan: {e}")
            return redirect(url_for('pemesanan'))

        finally:
            cursor.close()
            conn.close()

    # GET method
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if filter_nama:
            cursor.execute("SELECT * FROM barang WHERE stok > 0 AND nama LIKE %s", ('%' + filter_nama + '%',))
        else:
            cursor.execute("SELECT * FROM barang WHERE stok > 0")
        barang_list = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('pemesanan.html', barang=barang_list, filter_nama=filter_nama)


# ======================== CETAK STRUK ============================

@app.route('/cetak_struk/<int:pesanan_id>')
def cetak_struk(pesanan_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Ambil data pesanan
        cursor.execute("SELECT * FROM pesanan WHERE id = %s", (pesanan_id,))
        pesanan = cursor.fetchone()
        cursor.fetchall()  # Kosongkan sisa result (jika ada)

        if not pesanan:
            flash("Pesanan tidak ditemukan.")
            return redirect(url_for('pemesanan'))

        # Ambil detail pesanan
        cursor.execute("""
            SELECT dp.jumlah, dp.subtotal, b.nama, b.harga
            FROM detail_pesanan dp
            JOIN barang b ON dp.barang_id = b.id
            WHERE dp.pesanan_id = %s
        """, (pesanan_id,))
        detail = cursor.fetchall()

        return render_template('cetak_struk.html', pesanan=pesanan, detail=detail)

    except Exception as e:
        flash(f"Terjadi kesalahan saat mengambil data: {e}")
        return redirect(url_for('pemesanan'))

    finally:
        cursor.close()
        conn.close()

@app.route('/preview_struk/<int:pesanan_id>')
def preview_struk(pesanan_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM pesanan WHERE id = %s", (pesanan_id,))
        pesanan = cursor.fetchone()
        cursor.fetchall()  # Kosongkan hasil sisa query

        if not pesanan:
            flash("Pesanan tidak ditemukan.")
            return redirect(url_for('pemesanan'))

        cursor.execute("""
            SELECT dp.jumlah, dp.subtotal, b.nama, b.harga
            FROM detail_pesanan dp
            JOIN barang b ON dp.barang_id = b.id
            WHERE dp.pesanan_id = %s
        """, (pesanan_id,))
        detail = cursor.fetchall()

        return render_template('preview_struk.html', pesanan=pesanan, detail=detail)

    except Exception as e:
        flash(f"Terjadi kesalahan saat mengambil data: {e}")
        return redirect(url_for('pemesanan'))

    finally:
        cursor.close()
        conn.close()



# ======================== LAPORAN & EXPORT ============================
@app.route('/laporan')
def laporan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, p.tanggal, p.total,
                GROUP_CONCAT(CONCAT(b.nama, ' (', d.jumlah, ')') ORDER BY b.nama SEPARATOR ', ') AS isi
            FROM pesanan p
            JOIN detail_pesanan d ON p.id = d.pesanan_id
            JOIN barang b ON d.barang_id = b.id
            GROUP BY p.id, p.tanggal, p.total
            ORDER BY p.tanggal DESC
        """)
        data = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('laporan.html', laporan=data)


def get_laporan_data(tanggal_mulai, tanggal_akhir):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id AS id_pesanan, p.tanggal, p.total,
                   b.nama AS nama_barang, d.jumlah, d.subtotal
            FROM pesanan p
            JOIN detail_pesanan d ON p.id = d.pesanan_id
            JOIN barang b ON d.barang_id = b.id
            WHERE DATE(p.tanggal) BETWEEN %s AND %s
            ORDER BY p.tanggal DESC, p.id
        """, (tanggal_mulai, tanggal_akhir))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

@app.route('/export_laporan_harian')
def export_laporan_harian():
    tanggal = datetime.today().date()
    data = get_laporan_data(tanggal, tanggal)
    return generate_excel(data, f"Laporan_Harian_{tanggal}.xlsx")

@app.route('/export_laporan_mingguan')
def export_laporan_mingguan():
    tanggal_akhir = datetime.today().date()
    tanggal_mulai = tanggal_akhir - timedelta(days=6)  # 7 hari terakhir termasuk hari ini
    data = get_laporan_data(tanggal_mulai, tanggal_akhir)
    return generate_excel(data, f"Laporan_Mingguan_{tanggal_mulai}_sd_{tanggal_akhir}.xlsx")

def generate_excel(data, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Laporan Penjualan"

    # Header
    ws.append(["ID Pesanan", "Tanggal", "Nama Barang", "Jumlah", "Subtotal", "Total"])

    last_id = None
    for row in data:
        row_data = [
            row['id_pesanan'] if row['id_pesanan'] != last_id else "",
            row['tanggal'].strftime('%Y-%m-%d %H:%M:%S') if row['id_pesanan'] != last_id else "",
            row['nama_barang'],
            row['jumlah'],
            row['subtotal'],
            row['total'] if row['id_pesanan'] != last_id else "",
        ]
        ws.append(row_data)
        last_id = row['id_pesanan']

    # Simpan ke memori
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, download_name=filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
