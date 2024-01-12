from tkinter import messagebox
import mysql.connector
import tkinter as tk
from tkinter import simpledialog
from mysql.connector import errors
from datetime import datetime




class AplikasiManajemenPerpustakaan:
    def __init__(self, root):
        self.root = root
        self.root.title("APLIKASI SISTEM PEMINJAMAN BUKU")

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
        menu_bar.add_cascade(label="Home", menu=menu_file)
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
        menu_peminjam.add_command(label="Lihat Semua Peminjam", command=self.lihat_semua_peminjam) 
        # Menu Update Data
        menu_update_data = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Update Data", menu=menu_update_data)
        menu_update_data.add_command(label="Hapus Buku", command=self.hapus_buku)
        menu_update_data.add_command(label="Hapus Peminjam", command=self.hapus_peminjam)
        menu_update_data.add_command(label="Kembalikan Buku", command=self.kembalikan_buku)

        

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


        # Frame untuk mengupdate data buku
        self.frame_update_buku = tk.Frame(root)
        self.frame_update_buku.grid(row=0, column=2, padx=20, pady=20, sticky=tk.W)

        # Label dan Entry untuk ID Buku yang akan diupdate
        tk.Label(self.frame_update_buku, text="ID Buku yang akan diupdate:").grid(row=0, column=0, sticky=tk.E)
        self.entry_update_id_buku = tk.Entry(self.frame_update_buku)
        self.entry_update_id_buku.grid(row=0, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Judul Buku Baru
        tk.Label(self.frame_update_buku, text="Judul Buku Baru:").grid(row=1, column=0, sticky=tk.E)
        self.entry_update_judul_buku = tk.Entry(self.frame_update_buku)
        self.entry_update_judul_buku.grid(row=1, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Tahun Terbit Buku Baru
        tk.Label(self.frame_update_buku, text="Tahun Terbit Buku Baru:").grid(row=2, column=0, sticky=tk.E)
        self.entry_update_tahun_terbit_buku = tk.Entry(self.frame_update_buku)
        self.entry_update_tahun_terbit_buku.grid(row=2, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Penulis Buku Baru
        tk.Label(self.frame_update_buku, text="Penulis Buku Baru:").grid(row=3, column=0, sticky=tk.E)
        self.entry_update_penulis_buku = tk.Entry(self.frame_update_buku)
        self.entry_update_penulis_buku.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Tombol untuk mengupdate buku
        tk.Button(self.frame_update_buku, text="Update Data Buku", command=self.update_data_buku).grid(row=4, columnspan=2, pady=10)


        # Frame untuk mengupdate data peminjam
        self.frame_update_peminjam = tk.Frame(root)
        self.frame_update_peminjam.grid(row=0, column=3, padx=20, pady=20, sticky=tk.W)

        # Label dan Entry untuk ID Peminjam yang akan diupdate
        tk.Label(self.frame_update_peminjam, text="ID Peminjam yang akan diupdate:").grid(row=0, column=0, sticky=tk.E)
        self.entry_update_id_peminjam = tk.Entry(self.frame_update_peminjam)
        self.entry_update_id_peminjam.grid(row=0, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Nama Peminjam Baru
        tk.Label(self.frame_update_peminjam, text="Nama Peminjam Baru:").grid(row=1, column=0, sticky=tk.E)
        self.entry_update_nama_peminjam = tk.Entry(self.frame_update_peminjam)
        self.entry_update_nama_peminjam.grid(row=1, column=1, pady=5, sticky=tk.W)

        # Tombol untuk mengupdate peminjam
        tk.Button(self.frame_update_peminjam, text="Update Data Peminjam", command=self.update_data_peminjam).grid(row=2, columnspan=2, pady=10)




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



    def hapus_buku(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Buku yang akan dihapus
            id_buku = simpledialog.askinteger("Hapus Buku", "Masukkan ID Buku yang akan dihapus:")

            # Cek apakah buku masih dipinjam
            sql_cek_peminjaman = "SELECT * FROM peminjam_buku WHERE Id_Buku = %s"
            val_cek_peminjaman = (id_buku,)
            self.cursor.execute(sql_cek_peminjaman, val_cek_peminjaman)
            hasil_cek_peminjaman = self.cursor.fetchall()

            if hasil_cek_peminjaman:
                messagebox.showwarning("Hapus Buku", "Buku masih dipinjam. Hapus semua catatan peminjaman terlebih dahulu.")
            else:
                # Hapus buku dari tabel pinjam_buku
                sql_hapus_buku = "DELETE FROM pinjam_buku WHERE id_buku = %s"
                val_hapus_buku = (id_buku,)
                self.cursor.execute(sql_hapus_buku, val_hapus_buku)
                self.db.commit()

                messagebox.showinfo("Hapus Buku", "Buku berhasil dihapus.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Error: {e}")


    def kembalikan_buku(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Peminjam yang akan mengembalikan buku
            id_peminjam = simpledialog.askinteger("Kembalikan Buku", "Masukkan ID Peminjam yang mengembalikan buku:")

            # SQL untuk mengembalikan buku berdasarkan ID Peminjam
            sql = "DELETE FROM peminjam_buku WHERE id_peminjam = %s"
            val = (id_peminjam,)

            self.cursor.execute(sql, val)
            self.db.commit()

            messagebox.showinfo("Kembalikan Buku", "Buku berhasil dikembalikan.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def hapus_peminjam(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Peminjam yang akan dihapus
            id_peminjam = simpledialog.askinteger("Hapus Peminjam", "Masukkan ID Peminjam yang akan dihapus:")

            # SQL untuk menghapus peminjam berdasarkan ID
            sql_peminjam_buku = "DELETE FROM peminjam_buku WHERE id_peminjam = %s"
            val_peminjam_buku = (id_peminjam,)

            self.cursor.execute(sql_peminjam_buku, val_peminjam_buku)

            sql_peminjam = "DELETE FROM peminjam WHERE id_peminjam = %s"
            val_peminjam = (id_peminjam,)

            self.cursor.execute(sql_peminjam, val_peminjam)

            self.db.commit()

            messagebox.showinfo("Hapus Peminjam", "Peminjam berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")







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

        # Membuat frame untuk menempatkan label-label dengan warna latar belakang yang berbeda
        frame_data_buku = tk.Frame(pop_up)
        frame_data_buku.pack(padx=10, pady=10)

        # Daftar warna latar belakang yang berbeda
        warna_latarnya = ["#FFD700", "#98FB98", "#87CEEB", "#FFA07A"]  # Ganti dengan warna yang Anda inginkan

        # Membuat label-label untuk menampilkan data buku dengan warna latar belakang yang berbeda
        for i, data_buku in enumerate(self.hasil_lihat_buku):
            warna_latarnya_saat_ini = warna_latarnya[i % len(warna_latarnya)]  # Memastikan indeks tidak melebihi panjang daftar warna
            label_id = tk.Label(frame_data_buku, text=f"ID: {data_buku[0]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_id.pack(fill=tk.X)

            label_judul = tk.Label(frame_data_buku, text=f"Judul: {data_buku[1]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_judul.pack(fill=tk.X)

            label_tahun_terbit = tk.Label(frame_data_buku, text=f"Tahun Terbit: {data_buku[2]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_tahun_terbit.pack(fill=tk.X)

            label_penulis = tk.Label(frame_data_buku, text=f"Penulis: {data_buku[3]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_penulis.pack(fill=tk.X)

            # Membuat garis pembatas antar data buku
            tk.Frame(frame_data_buku, height=1, bd=1, relief="solid", pady=5).pack(fill=tk.X)

        # Membuat tombol untuk menutup pop-up
        tk.Button(pop_up, text="Tutup", command=pop_up.destroy).pack(pady=10)



        


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


    def pinjam_buku(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Buku dan ID Peminjam
            id_buku = simpledialog.askinteger("Pinjam Buku", "Masukkan ID Buku yang dipinjam:")
            id_peminjam = simpledialog.askinteger("Pinjam Buku", "Masukkan ID Peminjam:")

            waktu_sekarang = datetime.now()
            waktu_peminjaman = waktu_sekarang.date()

            sql = "INSERT INTO peminjam_buku (Id_Buku, Id_Peminjam, waktu_Peminjaman) VALUES (%s, %s, %s)"
            val = (id_buku, id_peminjam, waktu_peminjaman)

            self.cursor.execute(sql, val)
            self.db.commit()
            messagebox.showinfo("Pinjam Buku", "Buku berhasil dipinjam.")
        except errors.IntegrityError as e:
            messagebox.showerror("Error", "Gagal meminjam buku. Pastikan ID Buku dan ID Peminjam valid.")
            # Optionally, you can print the error message for debugging purposes:
            print(f"Error: {e}")

    def tambah_peminjam(self):
        # Menggunakan simpledialog untuk memasukkan Nama Peminjam
        nama_peminjam = simpledialog.askstring("Tambah Peminjam", "Masukkan Nama Peminjam:")

        sql = "INSERT INTO peminjam (nama) VALUES (%s)"
        val = (nama_peminjam,)

        self.cursor.execute(sql, val)
        self.db.commit()
        messagebox.showinfo("Tambah Peminjam", "Peminjam berhasil ditambahkan.")

    


    def tambah_peminjam(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Peminjam dan Nama Peminjam
            id_peminjam = simpledialog.askinteger("Tambah Peminjam", "Masukkan ID Peminjam:")
            nama_peminjam = simpledialog.askstring("Tambah Peminjam", "Masukkan Nama Peminjam:")

            if id_peminjam and nama_peminjam:
                # Memasukkan data peminjam ke database
                sql = "INSERT INTO peminjam (id_peminjam, nama) VALUES (%s, %s)"
                val = (id_peminjam, nama_peminjam)

                self.cursor.execute(sql, val)
                self.db.commit()
                messagebox.showinfo("Tambah Peminjam", "Peminjam berhasil ditambahkan.")
            else:
                messagebox.showwarning("Tambah Peminjam", "ID Peminjam dan Nama Peminjam tidak boleh kosong.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Error: {e}")

    def cari_peminjam(self):
        try:
            # Menggunakan simpledialog untuk memasukkan ID Peminjam
            id_peminjam = simpledialog.askinteger("Cari Peminjam", "Masukkan ID Peminjam:")
    
            sql = "SELECT peminjam.id_peminjam, peminjam.nama, peminjam_buku.id_buku, pinjam_buku.judul, peminjam_buku.waktu_peminjaman FROM peminjam JOIN peminjam_buku ON peminjam.id_peminjam = peminjam_buku.id_peminjam JOIN pinjam_buku ON peminjam_buku.id_buku = pinjam_buku.id_buku WHERE peminjam.id_peminjam = %s"
            val = (id_peminjam,)
    
            self.cursor.execute(sql, val)
            hasil = self.cursor.fetchall()
    
            if hasil:
                # Menampilkan informasi Peminjam dan Buku dalam popup
                data_popup = ""
                for data in hasil:
                    data_popup += f"ID Peminjam: {data[0]}\nNama Peminjam: {data[1]}\nID Buku: {data[2]}\nJudul Buku: {data[3]}\nTanggal Peminjaman: {data[4]}\n"
    
                messagebox.showinfo("Informasi Peminjam", f"Informasi untuk ID Peminjam {id_peminjam}:\n{data_popup}")
            else:
                messagebox.showinfo("Informasi Peminjam", f"Tidak ditemukan informasi untuk ID Peminjam {id_peminjam}")
        except ValueError:
            messagebox.showerror("Error", "Masukkan ID Peminjam yang valid.")




    def tampilkan_buku_dipinjam(self):
            try:
                # Menggunakan simpledialog untuk memasukkan ID Peminjam
                id_peminjam = simpledialog.askinteger("Cari Peminjam", "Masukkan ID Peminjam:")

                # Menggunakan simpledialog untuk memasukkan ID Peminjam
                sql_peminjam = "SELECT * FROM peminjam WHERE id_peminjam = %s"
                val_peminjam = (id_peminjam,)

                self.cursor.execute(sql_peminjam, val_peminjam)
                hasil_peminjam = self.cursor.fetchall()

                if hasil_peminjam:
                    # Membuat pop-up untuk menampilkan data peminjam dan buku yang dipinjam dalam bentuk tabel
                    pop_up = tk.Toplevel(self.root)
                    pop_up.title("Data Peminjam dan Buku Dipinjam")

                    # Membuat Text widget untuk menampilkan data peminjam dan buku yang dipinjam
                    text_area = tk.Text(pop_up, wrap=tk.WORD, width=60, height=10)

                    # Menambahkan header tabel
                    text_area.insert(tk.END, "ID Peminjam\t|\tNama Peminjam\t|\tID Buku\t|\tJudul Buku\t|\tTanggal Peminjaman\n")
                    text_area.insert(tk.END, "-"*100 + "\n")

                    for data_peminjam in hasil_peminjam:
                        text_area.insert(tk.END, f"{data_peminjam[0]}\t|\t{data_peminjam[1]}\t|\t")

                        # Tampilkan buku yang dipinjam
                        self.tampilkan_buku_dipinjam_detail(id_peminjam, text_area)

                    # Menampilkan Text widget
                    text_area.pack()
                else:
                    messagebox.showinfo("Data Peminjam", f"Tidak ada data peminjam dengan ID {id_peminjam}")
            except ValueError:
                messagebox.showerror("Error", "ID Peminjam harus berupa angka.")



    def tampilkan_buku_dipinjam_detail(self, id_peminjam, text_area):
        sql_buku = "SELECT pinjam_buku.id_buku, pinjam_buku.judul, peminjam_buku.waktu_Peminjaman FROM peminjam_buku JOIN pinjam_buku ON peminjam_buku.Id_Buku = pinjam_buku.id_buku WHERE peminjam_buku.Id_Peminjam = %s"
        val_buku = (id_peminjam,)

        self.cursor.execute(sql_buku, val_buku)
        hasil_buku = self.cursor.fetchall()

        if hasil_buku:
            for data_buku in hasil_buku:
                text_area.insert(tk.END, f"{data_buku[0]}\t|\t{data_buku[1]}\t|\t{data_buku[2]}\n")
        else:
            text_area.insert(tk.END, "Tidak ada buku yang dipinjam.\n")

    pass
    def update_data_buku(self):
        try:
            # Mengambil nilai dari Entry
            id_buku = int(self.entry_update_id_buku.get())
            judul_baru = self.entry_update_judul_buku.get()
            tahun_terbit_baru = int(self.entry_update_tahun_terbit_buku.get())
            penulis_baru = self.entry_update_penulis_buku.get()

            # Memperbarui data buku di database
            sql = "UPDATE pinjam_buku SET judul=%s, tahun_terbit=%s, penulis=%s WHERE id_buku=%s"
            val = (judul_baru, tahun_terbit_baru, penulis_baru, id_buku)

            self.cursor.execute(sql, val)
            self.db.commit()
            messagebox.showinfo("Update Data Buku", "Data buku berhasil diupdate.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai yang valid untuk Tahun Terbit.")

    def update_data_buku_gui(self):
        # Membuat pop-up baru untuk menginput data buku yang akan diupdate
        pop_up = tk.Toplevel(self.root)
        pop_up.title("Input Data Buku yang Akan Diupdate")

        # Frame untuk input data buku yang akan diupdate
        frame_update_buku = tk.Frame(pop_up)
        frame_update_buku.pack(padx=20, pady=20)

        # Menampilkan data buku untuk referensi
        self.lihat_semua_buku()

        # Label dan Entry untuk ID Buku
        tk.Label(frame_update_buku, text="ID Buku yang akan diupdate:").grid(row=0, column=0, sticky=tk.E)
        entry_id_buku = tk.Entry(frame_update_buku)
        entry_id_buku.grid(row=0, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Judul Buku Baru
        tk.Label(frame_update_buku, text="Judul Buku Baru:").grid(row=1, column=0, sticky=tk.E)
        entry_judul_buku_baru = tk.Entry(frame_update_buku)
        entry_judul_buku_baru.grid(row=1, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Tahun Terbit Buku Baru
        tk.Label(frame_update_buku, text="Tahun Terbit Buku Baru:").grid(row=2, column=0, sticky=tk.E)
        entry_tahun_terbit_buku_baru = tk.Entry(frame_update_buku)
        entry_tahun_terbit_buku_baru.grid(row=2, column=1, pady=5, sticky=tk.W)

        # Label dan Entry untuk Penulis Buku Baru
        tk.Label(frame_update_buku, text="Penulis Buku Baru:").grid(row=3, column=0, sticky=tk.E)
        entry_penulis_buku_baru = tk.Entry(frame_update_buku)
        entry_penulis_buku_baru.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Tombol untuk melakukan update
        tk.Button(frame_update_buku, text="Update Data Buku", command=lambda: self.update_data_buku(
            entry_id_buku.get(), entry_judul_buku_baru.get(), entry_tahun_terbit_buku_baru.get(),
            entry_penulis_buku_baru.get(), pop_up)).grid(row=4, columnspan=2, pady=10)
        
    def update_data_buku_callback(self):
        try:
            # Mengambil nilai dari Entry
            id_buku = int(self.entry_update_id_buku.get())
            judul_baru = self.entry_update_judul_buku.get()
            tahun_terbit_baru = int(self.entry_update_tahun_terbit_buku.get())
            penulis_baru = self.entry_update_penulis_buku.get()

            # Memperbarui data buku di database
            sql = "UPDATE pinjam_buku SET judul=%s, tahun_terbit=%s, penulis=%s WHERE id_buku=%s"
            val = (judul_baru, tahun_terbit_baru, penulis_baru, id_buku)

            self.cursor.execute(sql, val)
            self.db.commit()
            messagebox.showinfo("Update Data Buku", "Data buku berhasil diupdate.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai yang valid untuk ID Buku atau Tahun Terbit.")

    # def update_data_peminjam(self):
    #     # ... (your existing code)

    #     # Button to perform the update
    #     tk.Button(frame_update_peminjam, text="Update Data Peminjam", command=lambda: self.update_data_peminjam_db(entry_id_peminjam.get(), entry_nama_peminjam_baru.get(), entry_alamat_peminjam_baru.get(),entry_telepon_peminjam_baru.get(), pop_up)).grid(row=4, columnspan=2, pady=10)

    # def lihat_semua_peminjam(self):
    #     # Implement this method to retrieve and display borrower data
    #     pass

    def update_data_peminjam(self):
        try:
            # Mengambil nilai dari Entry
            id_peminjam = int(self.entry_update_id_peminjam.get())
            nama_peminjam_baru = self.entry_update_nama_peminjam.get()

            # Memperbarui data peminjam di database
            sql = "UPDATE peminjam SET nama=%s WHERE id_peminjam=%s"
            val = (nama_peminjam_baru, id_peminjam)

            self.cursor.execute(sql, val)
            self.db.commit()
            messagebox.showinfo("Update Data Peminjam", "Data peminjam berhasil diupdate.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai yang valid untuk ID Peminjam.")


    def lihat_semua_peminjam(self):
        try:
            # Retrieve all data of peminjam from the database
            self.cursor.execute("SELECT * FROM peminjam")
            hasil_lihat_peminjam = self.cursor.fetchall()
    
            if hasil_lihat_peminjam:
                # Create a string to display peminjam data
                data_peminjam_str = ""
                for data_peminjam in hasil_lihat_peminjam:
                    data_peminjam_str += f"ID Peminjam: {data_peminjam[0]}, Nama Peminjam: {data_peminjam[1]}\n"
    
                # Display peminjam data in a pop-up
                self.tampilkan_pop_up("Semua Peminjam", data_peminjam_str)
            else:
                messagebox.showinfo("Data Peminjam", "Tidak ada data peminjam.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # def tampilkan_pop_up(self, judul, isi):
    #     pop_up = tk.Toplevel(self.root)
    #     pop_up.title(judul)
    
    #     # Membuat frame untuk menempatkan label-label dengan warna latar belakang yang berbeda
    #     frame_data_peminjam = tk.Frame(pop_up)
    #     frame_data_peminjam.pack(padx=10, pady=10)
    
    #     # Daftar warna latar belakang yang berbeda
    #     warna_latarnya = ["#FFD700", "#98FB98", "#87CEEB", "#FFA07A"]  # Ganti dengan warna yang Anda inginkan
    
    #     # Membuat label-label untuk menampilkan data peminjam dengan warna latar belakang yang berbeda
    #     for i, data_peminjam in enumerate(hasil_lihat_peminjam):
    #         warna_latarnya_saat_ini = warna_latarnya[i % len(warna_latarnya)]  # Memastikan indeks tidak melebihi panjang daftar warna
    #         label_id_peminjam = tk.Label(frame_data_peminjam, text=f"ID Peminjam: {data_peminjam[0]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
    #         label_id_peminjam.pack(fill=tk.X)
    
    #         label_nama_peminjam = tk.Label(frame_data_peminjam, text=f"Nama Peminjam: {data_peminjam[1]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
    #         label_nama_peminjam.pack(fill=tk.X)
    
    #         # Membuat garis pembatas antar data peminjam
    #         tk.Frame(frame_data_peminjam, height=1, bd=1, relief="solid", pady=5).pack(fill=tk.X)
    
    #     # Membuat tombol untuk menutup pop-up
    #     tk.Button(pop_up, text="Tutup", command=pop_up.destroy).pack(pady=10)

        

    def lihat_semua_peminjam(self):
        try:
            # Mengambil semua data peminjam dari tabel peminjam
            self.cursor.execute("SELECT * FROM peminjam")
            hasil_lihat_peminjam = self.cursor.fetchall()

            if hasil_lihat_peminjam:
                # Menampilkan data peminjam dalam pop-up
                self.tampilkan_data_peminjam(hasil_lihat_peminjam)
            else:
                messagebox.showinfo("Data Peminjam", "Tidak ada data peminjam.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def tampilkan_data_peminjam(self, hasil_lihat_peminjam):
        pop_up = tk.Toplevel(self.root)
        pop_up.title("Semua Peminjam")

        frame_data_peminjam = tk.Frame(pop_up)
        frame_data_peminjam.pack(padx=10, pady=10)

        warna_latarnya = ["#FFD700", "#98FB98", "#87CEEB", "#FFA07A"]

        for i, data_peminjam in enumerate(hasil_lihat_peminjam):
            warna_latarnya_saat_ini = warna_latarnya[i % len(warna_latarnya)]
            label_id_peminjam = tk.Label(frame_data_peminjam, text=f"ID Peminjam: {data_peminjam[0]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_id_peminjam.pack(fill=tk.X)

            label_nama_peminjam = tk.Label(frame_data_peminjam, text=f"Nama Peminjam: {data_peminjam[1]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
            label_nama_peminjam.pack(fill=tk.X)

            # Membuat kueri SQL untuk mendapatkan judul buku yang dipinjam oleh peminjam
            sql_buku = "SELECT pinjam_buku.id_buku, pinjam_buku.judul FROM peminjam_buku JOIN pinjam_buku ON peminjam_buku.id_buku = pinjam_buku.id_buku WHERE peminjam_buku.id_peminjam = %s"
            val_buku = (data_peminjam[0],)

            self.cursor.execute(sql_buku, val_buku)
            hasil_buku = self.cursor.fetchall()

            if hasil_buku:
                for data_buku in hasil_buku:
                    label_judul_buku = tk.Label(frame_data_peminjam, text=f"Judul Buku: {data_buku[1]}", bd=1, relief="solid", padx=5, pady=5, bg=warna_latarnya_saat_ini)
                    label_judul_buku.pack(fill=tk.X)

            tk.Frame(frame_data_peminjam, height=1, bd=1, relief="solid", pady=5).pack(fill=tk.X)

        tk.Button(pop_up, text="Tutup", command=pop_up.destroy).pack(pady=10)


    def about_team(self):
        # Menampilkan notifikasi tentang tim dengan emoji
        messagebox.showinfo("About Team", "MADE By : KELOMPOk me ... 🚀")


if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = AplikasiManajemenPerpustakaan(root)
    root.mainloop()

