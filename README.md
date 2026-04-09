# 🐟 MiroFish V3 - Panduan Instalasi & Penggunaan

MiroFish V3 adalah aplikasi simulasi *Swarm AI* yang interaktif. Versi terbaru ini telah dioptimalkan agar **sangat mudah dijalankan** dengan satu perintah saja.

---

## 🏗️ Struktur Baru (Edisi Otomatis)
Sekarang Anda tidak perlu lagi mengatur Web Server terpisah. Server Python (`main.py`) sudah bertugas menangani semuanya:
- **Penyaji Web:** Menampilkan halaman MiroFish di browser.
- **Otak AI:** Menangani diskusi agen via DeepSeek API.
- **Deteksi Otomatis:** Frontend kini otomatis mendeteksi alamat servernya sendiri.

---

## 🚀 Langkah 1: Instalasi & Menjalankan (Sekali Klik)

### 1. Persiapan di VPS / Laptop
Pastikan sudah terinstall **Python 3.8+**.

### 2. Instalasi Dependensi
Buka terminal dan jalankan:
```bash
pip install fastapi uvicorn httpx
```

### 3. Pengaturan API Key DeepSeek (PENTING)
Agar aplikasi bisa memproses diskusi, Anda harus memasukkan API Key dari DeepSeek. Pilih salah satu cara di bawah ini:

#### A. Menggunakan Environment Variable (Paling Aman)
Cara ini sangat direkomendasikan agar API Key tidak tertulis langsung di file kode.
- **Linux / VPS Ubuntu:**
  ```bash
  export DEEPSEEK_API_KEY="isi_dengan_sk_anda_di_sini"
  ```
- **Windows (PowerShell - Umum digunakan di Tablet/Laptop Windows):**
  ```powershell
  $env:DEEPSEEK_API_KEY="isi_dengan_sk_anda_di_sini"
  ```
- **Windows (Command Prompt):**
  ```cmd
  set DEEPSEEK_API_KEY=isi_dengan_sk_anda_di_sini
  ```

#### B. Mengedit File Kode Secara Langsung
Jika cara di atas terlalu rumit, Anda bisa langsung mengedit file:
1. Buka file `backend/main.py`.
2. Cari baris: `DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "MASUKKAN_API_KEY_ANDA_DI_SINI")`.
3. Ganti teks `"MASUKKAN_API_KEY_ANDA_DI_SINI"` dengan API Key Anda, misal: `"sk-1234567890abcdef"`.
4. Simpan file.

### 4. Jalankan Aplikasi
```bash
cd microfish/backend
python main.py
```
Aplikasi kini aktif di port **8000**.

---

## 🌐 Langkah 2: Cara Mengakses

1.  Buka browser di **Tablet, HP, atau Laptop**.
2.  Ketik alamat IP perangkat yang menjalankan server tersebut.
    *Contoh: `http://192.168.100.155:8000`*
3.  Halaman MiroFish akan langsung muncul.
4.  **Selesai!** Anda tidak perlu lagi mengisi kotak "VPS Backend URL" secara manual karena sudah terdeteksi otomatis.

---

## 🎮 Fitur Utama MiroFish V3
- **🔊 Suara Agen (TTS):** Agen bicara dalam Bahasa Indonesia dengan karakter berbeda.
- **🛡️ Fokus Agen:** Setiap agen punya pendirian teguh (tidak plin-plan).
- **🎭 Mood Dinamis:** Emoji dan warna kanvas berubah sesuai emosi diskusi.
- **👑 Moderator Mode:** Anda memegang kendali penuh atas arah diskusi.

---

## 🛠️ Troubleshooting

| Masalah | Solusi |
| :--- | :--- |
| **Halaman tidak bisa dibuka di Tablet** | Pastikan Tablet dan Laptop terhubung ke Wi-Fi yang sama dan firewall port 8000 sudah dibuka. |
| **Suara tidak keluar** | Klik tombol "Mulai Sesi" atau "Suara Aktif". Browser mobile butuh interaksi pengguna untuk memulai audio. |
| **Error: API Key Missing** | Pastikan Anda sudah mengatur API Key di sisi server (VPS/Laptop), bukan di browser. |

---
*Dibuat untuk memudahkan simulasi AI yang seru dan interaktif!*
