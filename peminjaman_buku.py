import mysql.connector
from datetime import datetime
from prettytable import PrettyTable
import os

os.system("clear")


def koneksi():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        port=3306,
        database="peminjaman_buku",
    )
    return db


def tutupKoneksi(konek, cursor):
    cursor.close()
    konek.close()


# fungsi buku
def tambah_buku():
    konek = koneksi()
    cursor = konek.cursor()

    id_buku = int(input("Masukkan id buku : "))
    judul = input("Masukkan judu buku : ")
    tahun_terbit = int(input("Masukkan tahun terbit buku : "))
    penulis = input("Masukkan penulis buku : ")

    sql = """ INSERT INTO pinjam_buku (id_buku, judul, tahun_terbit, penulis) VALUES (%s,%s,%s,%s) """
    val_input = (id_buku, judul, tahun_terbit, penulis)
    cursor.execute(sql, val_input)
    print(f"Buku berhasil disimpan {cursor.rowcount}")
    konek.commit()
    tutupKoneksi(konek, cursor)


def lihat_semua_buku():
    konek = koneksi()
    cursor = konek.cursor()
    cursor.execute("SELECT * FROM pinjam_buku")
    hasil = cursor.fetchall()
    print("===================")
    print("SEMUA BUKU YANG TERSEDIA")
    if cursor.rowcount < 0:
        print("Tidak ada data buku")
    else:
        table = PrettyTable()
        table.field_names = ["Id Buku", "Judul", "Tahun Terbit", "Penulis"]
        table.align["Id Buku"] = "l"
        table.align["Judul"] = "l"
        table.align["Tahun Terbit"] = "l"
        table.align["Penulis"] = "l"
        for data_buku in hasil:
            table.add_row(
                [
                    f"{data_buku[0]}",
                    f"{data_buku[1]}",
                    f"{data_buku[2]}",
                    f"{data_buku[3]}",
                ]
            )
        print(table)
        print("==========================================")


def peminjam():
    konek = koneksi()
    cursor = konek.cursor()
    cursor.execute("SELECT * FROM peminjam")
    hasil = cursor.fetchall()
    if cursor.rowcount < 0:
        print("Tidak ada data peminjam")
    else:
        table = PrettyTable()
        table.field_names = ["Id Peminjam", "Nama"]
        table.align["Id Peminjam"] = "l"
        table.align["Nama"] = "l"
        for data_peminjam in hasil:
            table.add_row(
                [
                    f"{data_peminjam[0]}",
                    f"{data_peminjam[1]}",
                ]
            )
        print(table)


def input_peminjam():
    nama_peminjam = input("Masukkan nama peminjam buku : ")
    tambah_peminjam(nama_peminjam)


def tambah_peminjam(nama_peminjam):
    konek = koneksi()
    cursor = konek.cursor()
    sql = "INSERT INTO peminjam (nama) VALUES (%s)"
    input_val = (nama_peminjam,)
    cursor.execute(sql, input_val)
    konek.commit()
    tutupKoneksi(konek, cursor)


def buku_dipinjam():
    konek = koneksi()
    cursor = konek.cursor()
    lihat_semua_buku()
    idBuku = int(input("Masukkan id buku yang mau dipinjam : "))
    peminjam()
    idPeminjam = int(input("Masukkan id peminjam buku : "))
    waktuSekarang = datetime.now()
    waktu = waktuSekarang.date()
    sql = "INSERT INTO peminjam_buku (Id_Buku, Id_Peminjam, waktu_Peminjaman) VALUES (%s,%s,%s)"
    input_val = (idBuku, idPeminjam, waktu)
    cursor.execute(sql, input_val)
    konek.commit()
    tutupKoneksi(konek, cursor)


def cari_data_peminjam():
    konek = koneksi()
    cursor = konek.cursor()
    peminjam()
    id_peminjam = int(input("Masukkan id peminjam untuk mencari data : "))
    sql = f"""
        SELECT peminjam_buku.Id_Pinjam_Buku, peminjam.id_peminjam, peminjam.nama, pinjam_buku.id_buku, pinjam_buku.judul, pinjam_buku.penulis, pinjam_buku.tahun_terbit, peminjam_buku.waktu_Peminjaman 
        FROM peminjam_buku
        JOIN peminjam ON peminjam_buku.Id_Peminjam = peminjam.id_peminjam 
        JOIN pinjam_buku ON peminjam_buku.Id_Buku = pinjam_buku.id_buku WHERE peminjam.id_peminjam = {id_peminjam};
    """
    cursor.execute(sql)
    hasil = cursor.fetchall()
    if cursor.rowcount < 0:
        print("Tidak ada data peminjam")
    else:
        table = PrettyTable()
        table.field_names = [
            "Id Peminjaman",
            "Id Peminjam",
            "Nama",
            "Id Buku",
            "Judul",
            "Penulis",
            "Tahun Terbit",
            "Waktu Meminjam",
        ]
        table.align["Id Peminjaman"] = "l"
        table.align["Id Peminjam"] = "l"
        table.align["Nama"] = "l"
        table.align["Id Buku"] = "l"
        table.align["Judul"] = "l"
        table.align["Penulis"] = "l"
        table.align["Tahun Terbit"] = "l"
        table.align["Waktu Meminjam"] = "l"
        for data_peminjam_buku in hasil:
            table.add_row(
                [
                    f"{data_peminjam_buku[0]}",
                    f"{data_peminjam_buku[1]}",
                    f"{data_peminjam_buku[2]}",
                    f"{data_peminjam_buku[3]}",
                    f"{data_peminjam_buku[4]}",
                    f"{data_peminjam_buku[5]}",
                    f"{data_peminjam_buku[6]}",
                    f"{data_peminjam_buku[7]}",
                ]
            )
        print(table)


while True:
    print("SELAMAT DATANG DI SISTEM PEMINJAMAN")
    print("============ Menu ============")
    print("1. Tambah buku")
    print("2. Lihat semua buku")
    print("3. Tambah peminjam")
    print("4. Masukkan buku yang di pinjam")
    print("5. Cari data peminjam")
    print("0. keluar")
    print("===============================")

    pilihan = int(input("Masukkan menu yang anda pilih (0-4) : "))

    if pilihan == 1:
        tambah_buku()
    elif pilihan == 2:
        lihat_semua_buku()
    elif pilihan == 3:
        input_peminjam()
    elif pilihan == 4:
        buku_dipinjam()
    elif pilihan == 5:
        cari_data_peminjam()
