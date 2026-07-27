# Analisis Klaster Lokasi Gerai Kopi dan Deteksi Zona Sepi

**Nama :** Sindi Putri Diani

**NIM :** 23146035

**UAS :** Data Mining

**Kelas :** 01

## Penjelasan Proyek

Proyek ini menggunakan metode *clustering* **K-Means** untuk menganalisis
persebaran lokasi gerai kopi berdasarkan koordinat geografis (*latitude* dan
*longitude*). Hasil clustering digunakan untuk mengelompokkan gerai ke dalam
beberapa klaster wilayah, kemudian setiap klaster diklasifikasikan sebagai:

- **Zona Ramai** — klaster dengan jumlah gerai kopi di atas ambang batas
  tertentu (kepadatan gerai tinggi).
- **Zona Sepi** — klaster dengan jumlah gerai kopi di bawah ambang batas
  (kepadatan gerai rendah / berisiko sepi pelanggan atau kompetitor).

Aplikasi ini juga memungkinkan pengguna memasukkan koordinat lokasi baru,
lalu sistem akan memprediksi klaster terdekat dan status zona (ramai/sepi)
dari lokasi tersebut menggunakan model K-Means yang sudah dilatih.

## Fitur

1. Upload dataset gerai kopi (CSV: `nama, latitude, longitude`) atau gunakan
   data contoh (`sample_data.csv`) bawaan aplikasi.
2. Pengaturan jumlah klaster (K) dan ambang batas zona sepi secara interaktif.
3. Visualisasi klaster pada scatter plot latitude vs longitude, dengan warna
   berbeda untuk tiap klaster dan simbol berbeda untuk status ramai/sepi.
4. Ringkasan jumlah gerai dan status tiap klaster.
5. Form input lokasi baru untuk memprediksi klaster & status zona
   (ramai/sepi) secara langsung.

## Instruksi Menjalankan Aplikasi

### 1. Clone repository
```bash
git clone https://github.com/sindiputridiani109-sindi/Sindi-Putri-Diani.git
cd Sindi-Putri-Diani
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan aplikasi
```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`.

## Link Aplikasi Streamlit yang Aktif

[ https://sindi-putri-diani-qu6imgtkafjfakv9ujcrd8.streamlit.app/]

## Struktur File

```
├── app.py                     # Aplikasi utama Streamlit
├── generate_sample_data.py    # Script pembuat data contoh
├── sample_data.csv            # Data contoh gerai kopi (dummy)
├── requirements.txt           # Daftar dependency
└── README.md                  # Dokumentasi proyek
```
