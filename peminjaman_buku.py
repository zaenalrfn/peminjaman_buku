import mysql.connector
from prettytable import PrettyTable
from datetime import date


# Inisialisasi koneksi database
def buat_koneksi():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="peminjaman_buku"
    )


# Fungsi untuk menutup koneksi dan cursor
def tutup_koneksi(connection, cursor):
    cursor.close()
    connection.close()


# Fungsi untuk menampilkan semua buku dari database
def ambil_semua_buku_dari_db():
    connection = buat_koneksi()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM buku")
    result = cursor.fetchall()

    buku_dari_db = []
    for row in result:
        buku_dari_db.append(
            {
                "Kode Buku": row[0],
                "Judul": row[1],
                "Penerbit": row[2],
                "Pengarang": row[3],
                "Tahun": row[4],
            }
        )

    tutup_koneksi(connection, cursor)
    return buku_dari_db


# Fungsi untuk menyimpan buku ke database
def simpan_buku_ke_db(kd_buku, judul, penerbit, pengarang, tahun):
    connection = buat_koneksi()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO buku (kd_buku, judul, penerbit, pengarang, tahun) VALUES (%s, %s, %s, %s, %s)",
        (kd_buku, judul, penerbit, pengarang, tahun),
    )
    connection.commit()

    tutup_koneksi(connection, cursor)


# Fungsi untuk menghapus buku dari database
def hapus_buku_db(kode_buku):
    connection = buat_koneksi()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM buku WHERE kd_buku = %s", (kode_buku,))
    connection.commit()

    tutup_koneksi(connection, cursor)


# Fungsi untuk menampilkan semua buku
def tampilkan_semua_buku():
    buku = ambil_semua_buku_dari_db()
    if not buku:
        print("Tidak ada buku tersedia.")
    else:
        print("\n=== Semua Buku ===")
        table = PrettyTable()
        table.field_names = ["Kode Buku", "Judul", "Penerbit", "Pengarang", "Tahun"]
        table.align["Kode Buku"] = "l"
        table.align["Judul"] = "l"
        table.align["Penerbit"] = "l"
        table.align["Pengarang"] = "l"
        table.align["Tahun"] = "l"

        for book in buku:
            table.add_row(
                [
                    f"Kode Buku: {book['Kode Buku']}",
                    f"Judul: {book['Judul']}",
                    f"Penerbit: {book['Penerbit']}",
                    f"Pengarang: {book['Pengarang']}",
                    f"Tahun: {book['Tahun']}",
                ]
            )

        print(table)
        print("============================")


# Fungsi untuk menambahkan buku
def tambah_buku():
    kd_buku = input("Masukkan kode buku : ")
    judul = input("Masukkan judul buku: ")
    penerbit = input("Masukkan penerbit buku: ")
    pengarang = input("Masukkan pengarang buku: ")
    tahun = input("Masukkan tahun terbit buku: ")

    simpan_buku_ke_db(kd_buku, judul, penerbit, pengarang, tahun)
    print(f"Buku '{judul}' berhasil ditambahkan.")


# Fungsi untuk menghapus buku
def hapus_buku():
    buku = ambil_semua_buku_dari_db()
    tampilkan_semua_buku()

    # Ubah kode_buku menjadi string
    kode_buku = input("Masukkan kode buku yang ingin dihapus: ")

    # Periksa apakah kode buku ada di database sebelum menghapus
    if any(str(book["Kode Buku"]) == kode_buku for book in buku):
        hapus_buku_db(kode_buku)
        print(f"Buku dengan kode {kode_buku} berhasil dihapus.")

        # Perbarui variabel buku setelah penghapusan
        buku = ambil_semua_buku_dari_db()
        tampilkan_semua_buku()
    else:
        print(f"Buku dengan kode {kode_buku} tidak ditemukan.")


def tambah_peminjam():
    connection = buat_koneksi()
    cursor = connection.cursor()
    nama = input("Masukkan nama Peminjam : ")
    waktu = date.today()
    nama_buku = input("Masukkan nama buku yang dipinjam : ")
    kode_buku = input("Masukkan kode buku yang dipinjam : ")
    cursor.execute(
        """
            INSERT INTO peminjam (ID, Nama, Waktu, nama_buku, kd_buku)
            VALUES (%s, %s, %s, %s, %s)
        """,
        ("", nama, waktu, nama_buku, kode_buku),
    )
    connection.commit()


# Looping untuk interaksi dengan pengguna
while True:
    print("============================")
    print("| SISTEM PEMINJAMAN BUKU   |")
    print("============================")
    print("|1|. Tambah Peminjam Buku    |")
    print("|2|. Tampilkan Data Peminjam |")
    print("|3|. Tampilkan Semua Buku     |")
    print("|4|. Tambah Buku             |")
    print("|5|. Hapus Buku              |")
    print("|0|. Keluar                  |")
    print("============================")

    pilihan = input("Masukkan pilihan Anda (0-3): ")

    if pilihan == "1":
        tambah_peminjam()
    elif pilihan == "2":
        tampilkan_semua_buku()
    elif pilihan == "2":
        tambah_buku()
    elif pilihan == "3":
        hapus_buku()
    elif pilihan == "0":
        print("Terima kasih, sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
