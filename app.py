from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db_penelitian_dosen')

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    # Query join lengkap termasuk id_tim untuk tombol hapus
    cursor.execute('''
        SELECT t.id_tim, d.nama_dosen, k.judul_kegiatan, t.peran, k.status_kegiatan 
        FROM tim_kegiatan t
        JOIN dosen d ON t.id_dosen = d.id_dosen
        JOIN kegiatan k ON t.id_kegiatan = k.id_kegiatan
    ''')
    laporan = cursor.fetchall()
    
    # Ambil data untuk dropdown tambah
    cursor.execute("SELECT * FROM dosen")
    dosen_list = cursor.fetchall()
    cursor.execute("SELECT * FROM kegiatan")
    kegiatan_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('index.html', laporan=laporan, dosen_list=dosen_list, kegiatan_list=kegiatan_list)

@app.route('/tambah', methods=['POST'])
def tambah():
    id_dosen = request.form['id_dosen']
    id_kegiatan = request.form['id_kegiatan']
    peran = request.form['peran']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tim_kegiatan (id_dosen, id_kegiatan, peran) VALUES (%s, %s, %s)", (id_dosen, id_kegiatan, peran))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id_tim>', methods=['POST'])
def delete(id_tim):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tim_kegiatan WHERE id_tim = %s", (id_tim,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)