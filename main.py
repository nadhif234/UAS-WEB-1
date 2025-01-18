from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'nadhif'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'wisatategal'

mysql = MySQL(app)

# Route untuk cek koneksi ke database
@app.route('/cek_koneksi')
def cek_koneksi():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "Koneksi berhasil!"
    except Exception as e:
        return f"Koneksi gagal: {e}"

# Route untuk menampilkan halaman tambah, edit, dan hapus produk
@app.route('/admin', methods=['GET', 'POST'])
def manage_data():
    if request.method == 'POST':
        try:
            operation = request.form.get('operation')
            data_id = request.form.get('data_id')

            if operation == 'edit':
                # Edit data
                namalengkap = request.form.get('namalengkap')
                nomerhp = request.form.get('nomerhp')
                wisata = request.form.get('wisata')
                status = request.form.get('status')

                cur = mysql.connection.cursor()
                query_edit = """
                    UPDATE wisata_tegal
                    SET namalengkap = %s, nomerhp = %s, wisata = %s, status = %s
                    WHERE id = %s
                """
                cur.execute(query_edit, (namalengkap, nomerhp, wisata, status, data_id))
                mysql.connection.commit()
                cur.close()

                flash('Data berhasil diperbarui!', 'success')

            elif operation == 'delete':
                # Hapus data
                data_id = request.form.get('data_id')
                if not data_id:
                    flash('ID data tidak ditemukan', 'danger')
                    return redirect('/admin')

                cur = mysql.connection.cursor()
                query_delete = "DELETE FROM wisata_tegal WHERE id = %s"
                cur.execute(query_delete, (data_id,))
                mysql.connection.commit()
                cur.close()

                flash('Data berhasil dihapus!', 'success')

            elif operation == 'add':
                # Tambah data
                namalengkap = request.form.get('namalengkap')
                nomerhp = request.form.get('nomerhp')
                wisata = request.form.get('wisata')
                status = 'terpesan'  # Status default saat ditambahkan

                cur = mysql.connection.cursor()
                query_add = """
                    INSERT INTO wisata_tegal (namalengkap, nomerhp, wisata, status)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(query_add, (namalengkap, nomerhp, wisata, status))
                mysql.connection.commit()
                cur.close()

                flash('Data berhasil ditambahkan!', 'success')

            return redirect('/admin')

        except Exception as e:
            print("Error:", e)
            flash(f'Operasi gagal: {e}', 'danger')
            return redirect('/admin')

    else:
        try:
            # Ambil data dari database untuk ditampilkan di tabel
            cur = mysql.connection.cursor()
            query_fetch = "SELECT id, namalengkap, nomerhp, wisata, status FROM wisata_tegal"
            cur.execute(query_fetch)
            data = cur.fetchall()
            cur.close()

            # Kirim data ke template
            return render_template('admin.html', data=data)

        except Exception as e:
            print("Error:", e)
            flash(f'Gagal memuat data: {e}', 'danger')
            return render_template('admin.html', data=[])

# Route home
@app.route('/')
def home():
    return render_template('home.html')

# Route kontak
@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

# Route layanan untuk pemesanan tiket
@app.route('/layanan', methods=['GET', 'POST'])
def layanan():
    if request.method == 'POST':
        nama_lengkap = request.form.get('namalengkap')
        nomor_hp = request.form.get('nomerhp')
        wisata = request.form.get('wisata')

        # Simpan data pemesanan tiket ke dalam tabel wisata_tegal
        try:
            cur = mysql.connection.cursor()
            query_add = """
                INSERT INTO wisata_tegal (namalengkap, nomerhp, wisata, status)
                VALUES (%s, %s, %s, 'terpesan')
            """
            cur.execute(query_add, (nama_lengkap, nomor_hp, wisata))
            mysql.connection.commit()
            cur.close()

            flash('Pemesanan berhasil dilakukan!', 'success')

        except Exception as e:
            print(f"Error: {e}")
            flash(f'Pemesanan gagal: {e}', 'danger')

        return redirect('/layanan')  

    return render_template('layanan.html')

if __name__ == '__main__':
    app.run(debug=True)
