import mysql.connector
from datetime import datetime
from prettytable import PrettyTable
import os

os.system("clear")




def koneksi():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="peminjaman_buku_zdn",
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

def update_data_buku():
    konek = koneksi()
    cursor = konek.cursor()

    lihat_semua_buku()
    id_buku = int(input("Masukkan id buku yang ingin diupdate: "))
    
    judul = input("Masukkan judul buku baru: ")
    tahun_terbit = int(input("Masukkan tahun terbit buku baru: "))
    penulis = input("Masukkan penulis buku baru: ")

    sql = "UPDATE pinjam_buku SET judul=%s, tahun_terbit=%s, penulis=%s WHERE id_buku=%s"
    val_update = (judul, tahun_terbit, penulis, id_buku)
    cursor.execute(sql, val_update)

    konek.commit()
    print(f"Data buku dengan ID {id_buku} berhasil diupdate.")
    tutupKoneksi(konek, cursor)


def update_data_peminjam():
    konek = koneksi()
    cursor = konek.cursor()

    peminjam()
    id_peminjam = int(input("Masukkan id peminjam yang ingin diupdate: "))
    nama_peminjam_baru = input("Masukkan nama peminjam baru: ")

    sql = "UPDATE peminjam SET nama=%s WHERE id_peminjam=%s"
    val_update = (nama_peminjam_baru, id_peminjam)
    cursor.execute(sql, val_update)

    konek.commit()
    print(f"Data peminjam dengan ID {id_peminjam} berhasil diupdate.")
    tutupKoneksi(konek, cursor)


def cek_buku_dipinjam(id_buku):
    konek = koneksi()
    cursor = konek.cursor()
    sql = "SELECT COUNT(*) FROM peminjam_buku WHERE Id_Buku = %s"
    val_check = (id_buku,)
    cursor.execute(sql, val_check)
    hasil = cursor.fetchone()[0]
    tutupKoneksi(konek, cursor)
    return hasil > 0


def hapus_data_buku():
    konek = koneksi()
    cursor = konek.cursor()

    lihat_semua_buku()
    id_buku = int(input("Masukkan id buku yang ingin dihapus: "))

    if cek_buku_dipinjam(id_buku):
        print("Maaf, buku ini sedang dipinjam oleh seseorang. Tidak dapat dihapus.")
    else:
        sql = "DELETE FROM pinjam_buku WHERE id_buku=%s"
        val_delete = (id_buku,)
        cursor.execute(sql, val_delete)

        konek.commit()
        print(f"Data buku dengan ID {id_buku} berhasil dihapus.")
    
    tutupKoneksi(konek, cursor)


def hapus_data_peminjam():
    konek = koneksi()
    cursor = konek.cursor()

    peminjam()
    id_peminjam = int(input("Masukkan id peminjam yang ingin dihapus: "))

    # Cek apakah peminjam memiliki catatan peminjaman
    sql_cek_peminjaman = "SELECT COUNT(*) FROM peminjam_buku WHERE Id_Peminjam = %s"
    val_check_peminjaman = (id_peminjam,)
    cursor.execute(sql_cek_peminjaman, val_check_peminjaman)
    count_peminjaman = cursor.fetchone()[0]

    if count_peminjaman > 0:
        print("Maaf, peminjam ini masih memiliki catatan peminjaman. Tidak dapat dihapus.")
    else:
        # Hapus peminjam jika tidak ada catatan peminjaman terkait
        sql_hapus_peminjam = "DELETE FROM peminjam WHERE id_peminjam=%s"
        val_delete_peminjam = (id_peminjam,)
        cursor.execute(sql_hapus_peminjam, val_delete_peminjam)
        konek.commit()
        print(f"Data peminjam dengan ID {id_peminjam} berhasil dihapus.")

    tutupKoneksi(konek, cursor)

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
            

def lihat_data_peminjaman():
    konek = koneksi()
    cursor = konek.cursor()
    cursor.execute("SELECT * FROM peminjam_buku")
    hasil = cursor.fetchall()
    
    if cursor.rowcount < 0:
        print("Tidak ada data peminjaman")
    else:
        table = PrettyTable()
        table.field_names = [
            "Id Peminjaman",
            "Id Peminjam",
            "Id Buku",
            "Waktu Peminjaman"
        ]
        table.align["Id Peminjaman"] = "l"
        table.align["Id Peminjam"] = "l"
        table.align["Id Buku"] = "l"
        table.align["Waktu Peminjaman"] = "l"
        
        for data_peminjaman in hasil:
            table.add_row([
                f"{data_peminjaman[0]}",
                f"{data_peminjaman[1]}",
                f"{data_peminjaman[2]}",
                f"{data_peminjaman[3]}",
            ])
        
        print(table)

    tutupKoneksi(konek, cursor)


def pengembalian_buku():
    konek = koneksi()
    cursor = konek.cursor()
    lihat_data_peminjaman()
    id_peminjaman = int(input("Masukkan ID peminjaman yang akan dikembalikan: "))

    # Cek apakah peminjaman valid
    sql_cek_peminjaman = "SELECT * FROM peminjam_buku WHERE Id_Pinjam_Buku = %s"
    val_check_peminjaman = (id_peminjaman,)
    cursor.execute(sql_cek_peminjaman, val_check_peminjaman)
    peminjaman = cursor.fetchone()

    if not peminjaman:
        print("Peminjaman tidak ditemukan. Masukkan ID peminjaman yang valid.")
    else:
        # di sni code meLakukan pengembalian buku
        sql_pengembalian = "DELETE FROM peminjam_buku WHERE Id_Pinjam_Buku = %s"
        val_pengembalian = (id_peminjaman,)
        cursor.execute(sql_pengembalian, val_pengembalian)
        konek.commit()
        print(f"Buku dengan ID peminjaman {id_peminjaman} berhasil dikembalikan.")

    tutupKoneksi(konek, cursor)

def update_data_menu():
    while True:
        print("\n=========== Menu Update Data ===========")
        print("1. Update data buku")
        print("2. Update data peminjam")
        print("3. Pengembalian buku")
        print("4. Kembali ke menu utama")
        print("=========================================")

        pilihan_update = int(input("Masukkan menu yang anda pilih (1-4) : "))

        if pilihan_update == 1:
            update_data_buku()
        elif pilihan_update == 2:
            update_data_peminjam()
        elif pilihan_update == 3:
            pengembalian_buku()
        elif pilihan_update == 4:
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan antara 1-4.")


def hapus_data_menu():
    while True:
        print("\n=========== Menu Hapus Data ===========")
        print("1. Hapus data buku")
        print("2. Hapus data peminjam")
        print("3. Kembali ke menu utama")
        print("=========================================")

        pilihan_hapus = int(input("Masukkan menu yang anda pilih (1-3) : "))

        if pilihan_hapus == 1:
            hapus_data_buku()
        elif pilihan_hapus == 2:
            hapus_data_peminjam()
        elif pilihan_hapus == 3:
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan antara 1-3.")


while True:
    print("SELAMAT DATANG DI SISTEM PEMINJAMAN")
    print("============ Menu ============")
    print("1. Tambah buku")
    print("2. Lihat semua buku")
    print("3. Tambah peminjam")
    print("4. Masukkan buku yang di pinjam")
    print("5. Cari data peminjam")
    print("6. Update data")
    print("7. Hapus data")
    print("8. Keluar")
    print("===============================")

    pilihan = int(input("Masukkan menu yang anda pilih (0-8) : "))

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
    elif pilihan == 6:
        update_data_menu()
    elif pilihan == 7:
        hapus_data_menu()
    elif pilihan == 8:
        break
    else:
        print("Pilihan tidak valid. Silakan masukkan pilihan antara 0-8.")
