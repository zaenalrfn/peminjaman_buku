from tkinter import messagebox
import mysql.connector
import wx
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
####################################################################################################################################

class AplikasiPeminjamanBuku(wx.Frame):
    def __init__(self, parent, title):
        super(AplikasiPeminjamanBuku, self).__init__(parent, title=title, size=(600, 400))

        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)

        self.buat_halaman_tambah_buku()
        self.buat_halaman_lihat_buku()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        self.Centre()
        self.Show()

    def buat_halaman_tambah_buku(self):
        halaman = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        judul_label = wx.StaticText(halaman, label="Judul:")
        self.judul_entry = wx.TextCtrl(halaman)
        tahun_terbit_label = wx.StaticText(halaman, label="Tahun Terbit:")
        self.tahun_terbit_entry = wx.TextCtrl(halaman)
        penulis_label = wx.StaticText(halaman, label="Penulis:")
        self.penulis_entry = wx.TextCtrl(halaman)
        tambah_button = wx.Button(halaman, label="Tambah Buku")
        tambah_button.Bind(wx.EVT_BUTTON, self.tambah_buku)

        sizer.Add(judul_label, 0, wx.ALL, 5)
        sizer.Add(self.judul_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(tahun_terbit_label, 0, wx.ALL, 5)
        sizer.Add(self.tahun_terbit_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(penulis_label, 0, wx.ALL, 5)
        sizer.Add(self.penulis_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(tambah_button, 0, wx.ALL, 5)

        halaman.SetSizer(sizer)
        self.notebook.AddPage(halaman, "Tambah Buku")

    def buat_halaman_lihat_buku(self):
        halaman = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        lihat_button = wx.Button(halaman, label="Lihat Semua Buku")
        lihat_button.Bind(wx.EVT_BUTTON, self.lihat_semua_buku)

        sizer.Add(lihat_button, 0, wx.ALL, 5)

        halaman.SetSizer(sizer)
        self.notebook.AddPage(halaman, "Lihat Buku")

    def buat_halaman_tambah_peminjam(self):
        halaman = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        nama_label = wx.StaticText(halaman, label="Nama Peminjam:")
        self.nama_peminjam_entry = wx.TextCtrl(halaman)
        tambah_peminjam_button = wx.Button(halaman, label="Tambah Peminjam")
        tambah_peminjam_button.Bind(wx.EVT_BUTTON, self.tambah_peminjam)

        sizer.Add(nama_label, 0, wx.ALL, 5)
        sizer.Add(self.nama_peminjam_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(tambah_peminjam_button, 0, wx.ALL, 5)

    def buat_halaman_pinjam_buku(self):
        halaman = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        id_buku_label = wx.StaticText(halaman, label="ID Buku:")
        self.id_buku_entry = wx.TextCtrl(halaman)
        peminjam_id_label = wx.StaticText(halaman, label="ID Peminjam:")
        self.peminjam_id_entry = wx.TextCtrl(halaman)
        pinjam_buku_button = wx.Button(halaman, label="Masukkan Buku yang Dipinjam")
        pinjam_buku_button.Bind(wx.EVT_BUTTON, self.buku_dipinjam)

        sizer.Add(id_buku_label, 0, wx.ALL, 5)
        sizer.Add(self.id_buku_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(peminjam_id_label, 0, wx.ALL, 5)
        sizer.Add(self.peminjam_id_entry, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(pinjam_buku_button, 0, wx.ALL, 5)

        halaman.SetSizer(sizer)
        self.notebook.AddPage(halaman, "Masukkan Buku yang Dipinjam")

    def buat_halaman_cari_data_peminjam(self):
        halaman = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        id_peminjam_label = wx.StaticText(halaman, label="ID Peminjam:")
        self.id_peminjam_entry_cari = wx.TextCtrl(halaman)
        cari_data_peminjam_button = wx.Button(halaman, label="Cari Data Peminjam")
        cari_data_peminjam_button.Bind(wx.EVT_BUTTON, self.cari_data_peminjam)

        sizer.Add(id_peminjam_label, 0, wx.ALL, 5)
        sizer.Add(self.id_peminjam_entry_cari, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(cari_data_peminjam_button, 0, wx.ALL, 5)

        halaman.SetSizer(sizer)
        self.notebook.AddPage(halaman, "Cari Data Peminjam")

        halaman.SetSizer(sizer)
        self.notebook.AddPage(halaman, "Tambah Peminjam")

    def tambah_buku(self, event):
        judul = self.judul_entry.GetValue()
        tahun_terbit = self.tahun_terbit_entry.GetValue()
        penulis = self.penulis_entry.GetValue()

        try:
            # Koneksi ke database
            konek = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port=3306,
                database="peminjaman_buku_zdn",
            )
            
            # Membuat kursor
            cursor = konek.cursor()

            # Menjalankan query untuk menambahkan buku
            sql = """INSERT INTO pinjam_buku (judul, tahun_terbit, penulis) VALUES (%s, %s, %s)"""
            val_input = (judul, tahun_terbit, penulis)
            cursor.execute(sql, val_input)

            # Commit perubahan ke database
            konek.commit()

            # Menutup koneksi
            cursor.close()
            konek.close()

            wx.MessageBox("Buku berhasil ditambahkan!", "Info", wx.OK | wx.ICON_INFORMATION)

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            wx.MessageBox("Gagal menambahkan buku.", "Error", wx.OK | wx.ICON_ERROR)

    def lihat_semua_buku(self, event):
        try:
            # Koneksi ke database
            konek = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port=3306,
                database="peminjaman_buku_zdn",
            )

            # Membuat kursor
            cursor = konek.cursor()

            # Menjalankan query untuk melihat semua buku
            cursor.execute("SELECT * FROM pinjam_buku")
            hasil = cursor.fetchall()

            # Menampilkan hasil menggunakan PrettyTable
            if cursor.rowcount < 0:
                wx.MessageBox("Tidak ada data buku.", "Info", wx.OK | wx.ICON_INFORMATION)
            else:
                table = PrettyTable()
                table.field_names = ["ID Buku", "Judul", "Tahun Terbit", "Penulis"]
                for data_buku in hasil:
                    table.add_row([data_buku[0], data_buku[1], data_buku[2], data_buku[3]])

                wx.MessageBox(str(table), "Semua Buku", wx.OK | wx.ICON_INFORMATION)

            # Menutup koneksi
            cursor.close()
            konek.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            wx.MessageBox("Gagal mengambil data buku.", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    AplikasiPeminjamanBuku(None, title='Aplikasi Peminjaman Buku')
    app.MainLoop()

##################################################################################################################################3
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

# ... Bagian-bagian sebelumnya ...

def input_peminjam(self):
        nama_peminjam = self.nama_peminjam_entry.get()
        self.tambah_peminjam_database(nama_peminjam)
        messagebox.showinfo("Info", "Peminjam berhasil ditambahkan")

def buku_dipinjam(self):
        id_buku = self.id_buku_entry.get()
        peminjam_id = self.peminjam_id_entry.get()

        if not id_buku or not peminjam_id:
            messagebox.showerror("Error", "Masukkan ID Buku dan ID Peminjam untuk meminjam")
            return

        self.buku_dipinjam_database(id_buku, peminjam_id)
        messagebox.showinfo("Info", "Buku berhasil dipinjam")

def buku_dipinjam_database(self, id_buku, peminjam_id):
        konek = self.koneksi()
        cursor = konek.cursor()
        waktu_sekarang = datetime.now()
        waktu = waktu_sekarang.date()
        sql = "INSERT INTO peminjam_buku (Id_Buku, Id_Peminjam, waktu_Peminjaman) VALUES (%s, %s, %s)"
        input_val = (id_buku, peminjam_id, waktu)
        cursor.execute(sql, input_val)
        konek.commit()
        self.tutupKoneksi(konek, cursor)

def cari_data_peminjam(self):
        id_peminjam = self.id_peminjam_entry.get()

        if not id_peminjam:
            messagebox.showerror("Error", "Masukkan ID Peminjam untuk mencari data")
            return

        self.cari_data_peminjam_database(id_peminjam)

def cari_data_peminjam_database(self, id_peminjam):
        konek = self.koneksi()
        cursor = konek.cursor()
        sql = """
            SELECT peminjam_buku.Id_Pinjam_Buku, peminjam.id_peminjam, peminjam.nama, pinjam_buku.id_buku, pinjam_buku.judul, pinjam_buku.penulis, pinjam_buku.tahun_terbit, peminjam_buku.waktu_Peminjaman 
            FROM peminjam_buku
            JOIN peminjam ON peminjam_buku.Id_Peminjam = peminjam.id_peminjam 
            JOIN pinjam_buku ON peminjam_buku.Id_Buku = pinjam_buku.id_buku WHERE peminjam.id_peminjam = %s;
        """
        cursor.execute(sql, (id_peminjam,))
        hasil = cursor.fetchall()

        if cursor.rowcount < 0:
            messagebox.showinfo("Info", "Tidak ada data peminjam")
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
        messagebox.showinfo("Info", table)

        self.tutupKoneksi(konek, cursor)

# ... Bagian-bagian setelahnya ...



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


def hapus_data_buku():
    konek = koneksi()
    cursor = konek.cursor()

    lihat_semua_buku()
    id_buku = int(input("Masukkan id buku yang ingin dihapus: "))

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

    sql = "DELETE FROM peminjam WHERE id_peminjam=%s"
    val_delete = (id_peminjam,)
    cursor.execute(sql, val_delete)

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


def update_data_menu():
    while True:
        print("\n=========== Menu Update Data ===========")
        print("1. Update data buku")
        print("2. Update data peminjam")
        print("3. Kembali ke menu utama")
        print("=========================================")

        pilihan_update = int(input("Masukkan menu yang anda pilih (1-3) : "))

        if pilihan_update == 1:
            update_data_buku()
        elif pilihan_update == 2:
            update_data_peminjam()
        elif pilihan_update == 3:
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan pilihan antara 1-3.")


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
