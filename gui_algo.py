from tkinter import messagebox
import mysql.connector
import tkinter
import tkinter as tk
import wx.grid
from datetime import datetime
from prettytable import PrettyTable
import os



class AplikasiManajemenPerpustakaan:
    def __init__(self, root):
        self.root = root
        self.root.title("aplikasi.sistem peminjaman buku")

        # Inisialisasi koneksi database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="peminjaman_buku_zdn"
        )
        self.cursor = self.db.cursor()

        # Menu Bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        self.hasil_lihat_buku = []  # Variabel untuk menyimpan hasil query lihat buku

        # Menu File
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Keluar", command=root.destroy)

        # Menu Buku
        menu_buku = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Buku", menu=menu_buku)
        menu_buku.add_command(label="Tambah Buku", command=self.tambah_buku)
        menu_buku.add_command(label="Lihat Semua Buku", command=self.lihat_semua_buku)
        menu_buku.add_command(label="Pinjam Buku", command=self.pinjam_buku)

        # Menu Peminjam
        menu_peminjam = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Peminjam", menu=menu_peminjam)
        menu_peminjam.add_command(label="Tambah Peminjam", command=self.tambah_peminjam)
        menu_peminjam.add_command(label="Cari Peminjam", command=self.cari_peminjam)

        # Menu Update Data
        menu_update_data = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Update Data", menu=menu_update_data)
        menu_update_data.add_command(label="Update Data Buku", command=self.update_data_buku)
        menu_update_data.add_command(label="Update Data Peminjam", command=self.update_data_peminjam)

        

        # Menu Tentang
        menu_tentang = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tentang", menu=menu_tentang)
        menu_tentang.add_command(label="About Team", command=self.about_team)




# Frame untuk menambah buku
        self.frame_tambah_buku = tk.Frame(root)
        self.frame_tambah_buku.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W)

        # Label dan Entry untuk ID Buku
        tk.Label(self.frame_tambah_buku, text="ID Buku:").grid(row=0, column=0, sticky=tk.E)
        self.entry_id_buku = tk.Entry(self.frame_tambah_buku)
        self.entry_id_buku.grid(row=0, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Judul Buku
        tk.Label(self.frame_tambah_buku, text="Judul Buku:").grid(row=1, column=0, sticky=tk.E)
        self.entry_judul_buku = tk.Entry(self.frame_tambah_buku)
        self.entry_judul_buku.grid(row=1, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Tahun Terbit Buku
        tk.Label(self.frame_tambah_buku, text="Tahun Terbit Buku:").grid(row=2, column=0, sticky=tk.E)
        self.entry_tahun_terbit_buku = tk.Entry(self.frame_tambah_buku)
        self.entry_tahun_terbit_buku.grid(row=2, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Penulis Buku
        tk.Label(self.frame_tambah_buku, text="Penulis Buku:").grid(row=3, column=0, sticky=tk.E)
        self.entry_penulis_buku = tk.Entry(self.frame_tambah_buku)
        self.entry_penulis_buku.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Tombol untuk menambahkan buku
        tk.Button(self.frame_tambah_buku, text="Tambah Buku", command=self.tambah_buku).grid(row=4, columnspan=2, pady=10)

    def tambah_buku(self):
        # Mengambil nilai dari Entry
        id_buku = int(self.entry_id_buku.get())
        judul = self.entry_judul_buku.get()
        tahun_terbit = int(self.entry_tahun_terbit_buku.get())
        penulis = self.entry_penulis_buku.get()

        # Memasukkan data buku ke database
        sql = "INSERT INTO pinjam_buku (id_buku, judul, tahun_terbit, penulis) VALUES (%s, %s, %s, %s)"
        val = (id_buku, judul, tahun_terbit, penulis)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Tambah Buku", "Buku berhasil ditambahkan.")







    def lihat_semua_buku(self):
        self.cursor.execute("SELECT * FROM pinjam_buku")
        self.hasil_lihat_buku = self.cursor.fetchall()

        # Membuat string untuk menampilkan data buku dengan format yang diinginkan
        data_buku_str = ""
        for data_buku in self.hasil_lihat_buku:
            data_buku_str += f"ID: {data_buku[0]}\nJudul: {data_buku[1]}\nTahun Terbit: {data_buku[2]}\nPenulis: {data_buku[3]}\n\n"

        # Menampilkan data buku dalam pop-up
        self.tampilkan_pop_up("Semua Buku", data_buku_str)

    def tampilkan_pop_up(self, judul, isi):
        pop_up = tk.Toplevel(self.root)
        pop_up.title(judul)

        text_area = tk.Text(pop_up, wrap=tk.WORD, width=60, height=10)
        text_area.insert(tk.END, isi)
        text_area.pack()

    def pinjam_buku(self):
        id_buku = int(input("Masukkan ID Buku yang dipinjam: "))
        id_peminjam = int(input("Masukkan ID Peminjam: "))  

        waktu_sekarang = datetime.now()
        waktu_peminjaman = waktu_sekarang.date()

        sql = "INSERT INTO peminjam_buku (Id_Buku, Id_Peminjam, waktu_Peminjaman) VALUES (%s, %s, %s)"
        val = (id_buku, id_peminjam, waktu_peminjaman)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Pinjam Buku", "Buku berhasil dipinjam.")

    def tambah_peminjam(self):
        nama_peminjam = input("Masukkan Nama Peminjam: ")

        sql = "INSERT INTO peminjam (nama) VALUES (%s)"
        val = (nama_peminjam,)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Tambah Peminjam", "Peminjam berhasil ditambahkan.")

    def cari_peminjam(self):
        id_peminjam = int(input("Masukkan ID Peminjam: "))

        sql = "SELECT * FROM peminjam WHERE id_peminjam = %s"
        val = (id_peminjam,)

        self.cursor.execute(sql, val)
        hasil = self.cursor.fetchall()

        for data_peminjam in hasil:
            print(data_peminjam)

    def update_data_buku(self):
        id_buku = int(input("Masukkan ID Buku yang akan diupdate: "))
        judul_baru = input("Masukkan Judul Buku Baru: ")
        tahun_terbit_baru = int(input("Masukkan Tahun Terbit Buku Baru: "))
        penulis_baru = input("Masukkan Penulis Buku Baru: ")

        sql = "UPDATE pinjam_buku SET judul=%s, tahun_terbit=%s, penulis=%s WHERE id_buku=%s"
        val = (judul_baru, tahun_terbit_baru, penulis_baru, id_buku)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Update Data Buku", "Data buku berhasil diupdate.")

    def update_data_peminjam(self):
        id_peminjam = int(input("Masukkan ID Peminjam yang akan diupdate: "))
        nama_peminjam_baru = input("Masukkan Nama Peminjam Baru: ")

        sql = "UPDATE peminjam SET nama=%s WHERE id_peminjam=%s"
        val = (nama_peminjam_baru, id_peminjam)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Update Data Peminjam", "Data peminjam berhasil diupdate.")

    def about_team(self):
        # Menampilkan notifikasi tentang tim dengan emoji
        messagebox.showinfo("About Team", "DI BUAT OLEH KELOMPOK ... 🚀")


if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = AplikasiManajemenPerpustakaan(root)
    root.mainloop()

