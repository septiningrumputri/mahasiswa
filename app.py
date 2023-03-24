from flask import Flask
from flask import render_template, request, redirect, flash, session
from flask_session import Session

# koneksi database
from db import connection, cursor

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

@app.route("/login", methods=['GET', 'POST'])
def login():
    context = {}
    context['title'] = "Login"

    if request.method == "POST":
        param = request.form
        sql = "SELECT * FROM user WHERE username=%s AND password=%s"
        cursor.execute(sql, (
            param.get("username"),
            param.get("password")
        ))

        hasil = cursor.fetchall()
        if len(hasil) > 0:
            session['login'] = True
            return redirect("/")
        else:
            flash("Username atau password salah")

    return render_template("login.html", context=context)

@app.route("/")
def index_page():
    # mengambil data dari database
    sql = "SELECT * FROM calon_siswa ORDER BY id DESC"
    cursor.execute(sql)

    # parameter untuk views
    context = {}
    context['title'] = "Data Mahasiswa Baru"
    context['data'] = cursor.fetchall()
    if not session.get("login"):
        return redirect("/login")
    else:
        return render_template("index.html", context=context)

@app.route("/mahasiswa-baru", methods=["GET", "POST"])
def mahasiswa_baru():
    context = {}
    context['title'] = 'Tambahkan Mahasiswa Baru'

    # mengambil parameter request jika method nya post
    if request.method == "POST":
        param = request.form
        sql = "INSERT INTO `calon_siswa` (`nama`, `alamat`, `jenis_kelamin`, `agama`, `sekolah_asal`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,(
            param.get("nama"),
            param.get("alamat"),
            param.get("kelamin"),
            param.get("agama"),
            param.get("sekolah")
        ))
        connection.commit()
        return redirect("/")

    if not session.get("login"):
        return redirect("/login")
    else:
        return render_template("input.html", context=context)

@app.route("/update", methods=['GET', 'POST'])
def update():

    # mengambil data dari database
    sql = "SELECT * FROM calon_siswa WHERE id = %s"
    cursor.execute(sql, (request.args.get("id")))
    hasil = cursor.fetchone()

    # parameter untuk views
    context = {}
    context['title'] = "Edit data mahasiswa"
    context['data'] = hasil
    context['id'] = request.args.get("id")

    # update data jika method request POST
    if request.method == "POST":
        param = request.form
        sql = "UPDATE `calon_siswa` SET nama=%s, alamat=%s, jenis_kelamin=%s, agama=%s, sekolah_asal=%s WHERE id = %s"
        cursor.execute(sql, (
            param.get("nama"),
            param.get("alamat"),
            param.get("kelamin"),
            param.get("agama"),
            param.get("sekolah"),
            param.get("siswa_id"),
        ))
        connection.commit()

        return redirect("/")

    if not session.get("login"):
        return redirect("/login")
    else:
        return render_template("update.html", context=context)

@app.route("/delete", methods=['GET'])
def hapus_data():
    sql = "DELETE FROM `calon_siswa` WHERE id = %s"
    cursor.execute(sql, (request.args.get("id")))
    connection.commit()
    return redirect("/")