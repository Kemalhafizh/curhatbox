# 💜 CurhatBox: Premium Anonymous Messaging Platform

**CurhatBox** adalah platform web modern untuk pengiriman pesan rahasia secara anonim. Dibangun dengan fokus utama pada **Keamanan Tingkat Tinggi (Anti-Spam)**, **Analitik Mendalam (Creator Studio)**, dan **Estetika SaaS Premium**, aplikasi ini memungkinkan pengguna untuk menerima masukan jujur dari teman, membalasnya, serta membagikannya langsung ke Instagram Story.

Tidak seperti platform pesan anonim standar, CurhatBox dilengkapi dengan desain *Glassmorphism*, fitur penghancur pesan otomatis (*Self-Destruct*), hingga deteksi sentimen emoji.

---

## ✨ Fitur Premium (Highlight)

1. 🎨 **Modern SaaS UI/UX (Glassmorphism & Animated Mesh)**
   Antarmuka web telah direkayasa ulang menggunakan estetika *Software as a Service* (SaaS) tahun 2026. Latar belakang *Animated Mesh Gradient* dipadukan dengan panel tembus pandang (*Glassmorphism*) dan tipografi Google Fonts (*Outfit* & *Inter*) memberikan pengalaman visual tingkat elit yang *fluid* di desktop maupun *mobile*.

2. 📊 **Studio Analitik Penggemar (Creator Insights)**
   Dilengkapi dengan *dashboard* intelijen visual bertenaga **Chart.js**. Pengguna dapat melacak:
   - **Pertumbuhan Curhatan (Tren 7 Hari)**
   - **Sentimen Emoji (Doughnut Chart)** dari Reaksi Cepat.
   - **Jam Puncak (Radar Chart)** untuk melihat kapan penggemar paling aktif.
   - **Distribusi Browser & OS** dari para pengirim rahasia (*Sender Hints*).

3. 🧨 **Pesan Sekali Baca (Self-Destruct Messages)**
   Privasi tingkat militer ala Snapchat. Pengirim dapat memilih mengirim "Pesan Bom Waktu" yang hanya dapat dibaca **SATU KALI** oleh penerima. Setelah dibuka di Dasbor, pesan tersebut akan **dihapus secara permanen dari *Database*** tanpa sisa rekam jejak.

4. 🛡️ **Sistem Keamanan Anti-Spam Berlapis**
   - **Google reCAPTCHA v3**: Memblokir serangan *bot/script* secara senyap di latar belakang.
   - **Rate Limiting**: Membatasi IP agresif (maksimal 3 pesan per menit) untuk menghindari *spam/flood*.
   - **Firewall Blokir Mandiri**: Pemilik tautan dapat memblokir *IP Address* pengirim spesifik hanya dengan satu klik.
   - **Sensor Kata Cerdas**: Algoritma penyaringan kata-kata kotor/toksik yang aktif secara konstan.

5. ⚡ **Interaksi Dinamis & Reaksi Ekstra**
   Tidak perlu mengetik balasan panjang? Gunakan fitur **Quick Reactions** (berisi 15+ variasi emoji) yang akan menyalakan animasi hujan *Confetti* saat halaman pesan dibagikan ke publik.

6. 📱 **IG Story Ready & Kustomisasi Profil**
   Pesan langsung dikonversi menjadi gambar HTML Canvas siap-unduh untuk di-*share* ke IG Story. Pengguna juga bebas mengganti **Avatar** diri dan warna latar belakang profil mereka (Hex Theme Color).

---

## 🛠️ Stack Teknologi (Tech Stack)

Proyek ini dibangun menggunakan susunan lapisan teknologi modern:

- **Backend / Core**: Python 3.10+, Django 6.0
- **Database**: SQLite3 (Development) / PostgreSQL (Production-Ready)
- **Frontend Framework**: Bootstrap 5, Vanilla CSS3 (Custom Glass Utilities), HTML5
- **Frontend Libraries**: Chart.js (Data Vis), AOS (Animate on Scroll), HTML2Canvas (IG Story Generation), Canvas-Confetti
- **Security & Utils**: `django-ratelimit`, `user-agents`, `python-dotenv`, Google reCAPTCHA

---

## 📦 Panduan Instalasi & Menjalankan di Local

Ingin mencoba mengutak-atik atau menjalankan CurhatBox di komputer lokal Anda? Ikuti panduan instalasi di bawah ini.

### Prasyarat (Prerequisites)
- Python 3.10 atau lebih tinggi sudah terpasang di sistem.
- `pip` dan `virtualenv`.

### 1. Clone Repository
```bash
git clone https://github.com/Kemalhafizh/curhatbox.git
cd curhatbox
```

### 2. Buat & Aktifkan Virtual Environment
Sangat disarankan memakai *virtual environment* untuk menjaga dependensi tetap terisolasi.
```bash
# Pengguna Windows:
python -m venv venv
.\venv\Scripts\activate

# Pengguna Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependensi (Requirements)
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variables (.env)
Buka *root directory* proyek dan buat sebuah file bernama `.env`. Tambahkan kredensial keamanan berikut (ubah nilai aslinya untuk lingkungan produksi sejati):
```env
# Security Settings
SECRET_KEY=django-insecure-kunci-rahasia-anda-disini-12345
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Migrasi Database Skema
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Menjalankan Development Server
```bash
python manage.py runserver
```
🔥 **Aplikasi kini hidup!** Buka browser kesayangan Anda dan akses: `http://127.0.0.1:8000/`

---

## 🔒 Laporan Standar Keamanan & Audit
Proyek ini telah melalui proses audit kode dan telah mengimplementasikan pertahanan terhadap Kerentanan Web Standar (OWASP):
- **XSS (Cross-Site Scripting) Prevention**: Semua input pesan di-_escape_ saat render Dashboard maupun Profil Publik.
- **CSRF (Cross-Site Request Forgery) Tokens**: Diaktifkan secara keras pada setiap *State-Changing Form* (Autentikasi & Kirim Pesan).
- **IDOR (Insecure Direct Object Reference)**: Otorisasi *Backend* dikunci menempel absolut pada `request.user`. Pengguna tidak dapat memanipulasi *query parameter ID* untuk menghapus atau membaca pesan orang lain.
- **Secret Management**: Tidak ada kunci rahasia yang ter-_hardcode_ di basis kode (`settings.py`), sepenuhnya dialihkan ke variabel *Environment*.

---

<p align="center">
  Didesain dan dikembangkan dengan ❤️ oleh <b>Kemal Hafizh</b>.<br/>
  <i>Inisiatif Open Source untuk Portofolio Perangkat Lunak 2026.</i>
</p>