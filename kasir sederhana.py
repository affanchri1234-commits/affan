"""
SISTEM PEMESANAN MAKANAN SEDERHANA (OOP Python)

Konsep OOP yang diterapkan:
- 3 class        : MenuItem, Pesanan, Restoran
- Constructor    : __init__() di setiap class
- Attribute      : nama, harga, kategori, nama_pelanggan, dst.
- Method         : tampilkan_info(), tambah_item(), hitung_total(), dst.
- Encapsulation  : attribute private (diawali __) seperti __harga, __daftar_item
- Property/Setter: MenuItem.harga, Pesanan.nama_pelanggan
- Class method   : MenuItem.dari_string(), Pesanan.jumlah_pesanan()
- Static method  : Pesanan.format_rupiah(), Pesanan.hitung_pajak()
"""


class MenuItem:
    """Representasi satu menu makanan/minuman."""

    def __init__(self, nama, harga, kategori="Makanan"):
        self.nama = nama
        self.kategori = kategori
        self.__harga = 0          # private attribute (encapsulation)
        self.harga = harga        # lewat setter agar divalidasi

    # ---------- Property & Setter ----------
    @property
    def harga(self):
        """Getter: mengambil harga (attribute private)."""
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        """Setter: harga harus angka dan lebih dari 0."""
        if not isinstance(nilai, (int, float)) or nilai <= 0:
            raise ValueError("Harga harus berupa angka lebih dari 0!")
        self.__harga = nilai

    # ---------- Class Method ----------
    @classmethod
    def dari_string(cls, teks):
        """Membuat object MenuItem dari teks 'nama,harga,kategori'."""
        nama, harga, kategori = teks.split(",")
        return cls(nama.strip(), int(harga), kategori.strip())

    # ---------- Method biasa ----------
    def tampilkan_info(self):
        return f"{self.nama:<18} [{self.kategori:<7}] {Pesanan.format_rupiah(self.harga)}"


class Pesanan:
    """Representasi satu pesanan milik pelanggan."""

    PAJAK_PERSEN = 10          # class attribute
    __jumlah = 0               # private class attribute (penghitung pesanan)

    def __init__(self, nama_pelanggan):
        self.__nama_pelanggan = ""
        self.nama_pelanggan = nama_pelanggan   # lewat setter
        self.__daftar_item = []                # private: list of (MenuItem, jumlah)
        Pesanan.__jumlah += 1
        self.nomor = Pesanan.__jumlah

    # ---------- Property & Setter ----------
    @property
    def nama_pelanggan(self):
        return self.__nama_pelanggan

    @nama_pelanggan.setter
    def nama_pelanggan(self, nilai):
        if not nilai or not nilai.strip():
            raise ValueError("Nama pelanggan tidak boleh kosong!")
        self.__nama_pelanggan = nilai.strip().title()

    @property
    def daftar_item(self):
        """Read-only: mengembalikan salinan agar data asli aman."""
        return list(self.__daftar_item)

    # ---------- Class Method ----------
    @classmethod
    def jumlah_pesanan(cls):
        """Menampilkan total pesanan yang pernah dibuat."""
        return cls.__jumlah

    # ---------- Static Method ----------
    @staticmethod
    def format_rupiah(angka):
        """Mengubah angka menjadi format Rupiah, contoh: Rp 15.000"""
        return "Rp " + f"{angka:,.0f}".replace(",", ".")

    @staticmethod
    def hitung_pajak(subtotal, persen):
        """Menghitung pajak dari subtotal."""
        return subtotal * persen / 100

    # ---------- Method biasa ----------
    def tambah_item(self, menu_item, jumlah=1):
        if jumlah <= 0:
            raise ValueError("Jumlah pesanan harus lebih dari 0!")
        self.__daftar_item.append((menu_item, jumlah))

    def hitung_subtotal(self):
        return sum(item.harga * jml for item, jml in self.__daftar_item)

    def hitung_total(self):
        subtotal = self.hitung_subtotal()
        return subtotal + Pesanan.hitung_pajak(subtotal, Pesanan.PAJAK_PERSEN)

    def cetak_struk(self):
        garis = "=" * 46
        print(garis)
        print(f"STRUK PESANAN #{self.nomor}".center(46))
        print(garis)
        print(f"Pelanggan : {self.nama_pelanggan}")
        print("-" * 46)
        for item, jml in self.__daftar_item:
            baris = f"{item.nama} x{jml}"
            harga = Pesanan.format_rupiah(item.harga * jml)
            print(f"{baris:<28}{harga:>18}")
        print("-" * 46)
        subtotal = self.hitung_subtotal()
        pajak = Pesanan.hitung_pajak(subtotal, Pesanan.PAJAK_PERSEN)
        print(f"{'Subtotal':<28}{Pesanan.format_rupiah(subtotal):>18}")
        print(f"{'Pajak ' + str(Pesanan.PAJAK_PERSEN) + '%':<28}{Pesanan.format_rupiah(pajak):>18}")
        print(f"{'TOTAL BAYAR':<28}{Pesanan.format_rupiah(self.hitung_total()):>18}")
        print(garis)


class Restoran:
    """Mengelola daftar menu dan pesanan."""

    def __init__(self, nama):
        self.nama = nama
        self.__menu = {}          # private: nomor -> MenuItem
        self.__riwayat = []       # private: daftar Pesanan

    def tambah_menu(self, menu_item):
        nomor = len(self.__menu) + 1
        self.__menu[nomor] = menu_item

    def ambil_menu(self, nomor):
        if nomor not in self.__menu:
            raise KeyError("Nomor menu tidak ditemukan!")
        return self.__menu[nomor]

    def tampilkan_menu(self):
        print(f"\n===== MENU {self.nama.upper()} =====")
        for nomor, item in self.__menu.items():
            print(f"{nomor}. {item.tampilkan_info()}")

    def simpan_pesanan(self, pesanan):
        self.__riwayat.append(pesanan)

    def total_pendapatan(self):
        return sum(p.hitung_total() for p in self.__riwayat)


# ======================= PROGRAM UTAMA =======================
def buat_pesanan_interaktif(restoran):
    nama = input("\nMasukkan nama pelanggan: ")
    pesanan = Pesanan(nama)          # setter akan memvalidasi nama

    while True:
        restoran.tampilkan_menu()
        pilihan = input("\nPilih nomor menu (0 = selesai): ").strip()
        if pilihan == "0":
            break
        try:
            menu = restoran.ambil_menu(int(pilihan))
            jumlah = int(input(f"Jumlah {menu.nama}: "))
            pesanan.tambah_item(menu, jumlah)
            print(f"-> {menu.nama} x{jumlah} ditambahkan.")
        except (ValueError, KeyError) as e:
            print(f"[Error] {e}")

    if pesanan.daftar_item:
        pesanan.cetak_struk()
        restoran.simpan_pesanan(pesanan)
    else:
        print("Tidak ada item yang dipesan.")


def main():
    restoran = Restoran("Warung apan")

    # Object MenuItem dibuat lewat constructor biasa
    restoran.tambah_menu(MenuItem("Nasi Goreng", 15000, "Makanan"))
    restoran.tambah_menu(MenuItem("Sate Bandeng", 20000, "Makanan"))
    # Object MenuItem dibuat lewat class method
    restoran.tambah_menu(MenuItem.dari_string("Es Teh Manis, 5000, Minuman"))
    restoran.tambah_menu(MenuItem.dari_string("Jus Jeruk, 10000, Minuman"))

    print("=== SELAMAT DATANG DI SISTEM PEMESANAN MAKANAN ===")
    while True:
        print("\n1. Buat pesanan baru")
        print("2. Lihat total pembayaran")
        print("3. Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            buat_pesanan_interaktif(restoran)
        elif pilih == "2":
            print(f"Jumlah pesanan : {Pesanan.jumlah_pesanan()}")
            print(f"Total pembayaran: {Pesanan.format_rupiah(restoran.total_pendapatan())}")
        elif pilih == "3":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()