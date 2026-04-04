<div align="center">
  <img src="https://img.icons8.com/clouds/200/mailbox-closed-flag-up.png" alt="CurhatBox Logo" width="150"/>
  <h1>💜 CurhatBox v6.9 (Production Ready)</h1>
  <p><strong>Platform Pesan Anonim Premium Berkualitas SaaS dengan Keamanan Anti-Spam Tingkat Lanjut</strong></p>
  
  <p>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
    <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  </p>
</div>

---

## 📖 Apa itu CurhatBox?

**CurhatBox** adalah platform pengiriman pesan rahasia secara anonim (seperti Secreto atau NGL) namun telah direkayasa ulang untuk standar keamanan industri tahun 2026. Dibangun menggunakan arsitektur **Django ASGI (Daphne)**, platform ini menawarkan pengalaman yang interaktif, *real-time*, dan sangat tangguh terhadap ancaman *spam* maupun *cyberbullying*.

Dengan estetika antarmuka bergaya *Glassmorphism* dan dukungan multi-bahasa, CurhatBox dirancang tidak hanya sebagai alat hiburan untuk *Instagram Story*, tetapi juga sebagai **Creator Tool** yang andal dengan analitik mendalam.

---

## ✨ Fitur-Fitur Premium (Key Features)

### 1. 🎨 Modern SaaS UI/UX (Glassmorphism & Asynchronous UI)
Antarmuka web menggunakan fondasi **Bootstrap 5.3** yang disuntikkan secara kustom dengan utilitas *Glassmorphism*, palet gradasi *liquid*, serta dukungan mutlak untuk tema Terang (Light) dan Gelap (Dark). Transisi halaman ditenagai oleh animasi **AOS (Animate On Scroll)**.

### 2. 🔐 Keamanan & Autentikasi Kelas Enterprise
Sistem pengguna (*User Management*) telah dikembangkan secara masif, meliputi:
- **Pendaftaran & Log Masuk** dengan validasi ketat.
- **Lupa Password (Email Provider)**: Integrasi SMTP TLS Port 587 untuk mengirimkan instruksi ganti sandi menggunakan *template* email HTML yang responsif dan cantik.
- **Smart Resend Cooldown**: Pengiriman ulang email pemulihan dibatasi secara cerdas dengan jeda *cooldown* 60 detik berbasis memori tinggi menggunakan **Redis**, dilengkapi indikator hitung mundur di layar.
- **Ganti Password Internal**: Pengguna dengan status login dapat memperbarui *password* langsung dari halaman pengaturan tanpa harus keluar (logout).

### 3. 🌐 Global Multilingual System (i18n)
CurhatBox tidak dibatasi oleh batas negara. Tersedia utilitas alih bahasa (*Language Switcher*) yang elegan di bagian _footer_, memungkinkan seluruh konten beradaptasi secara otomatis. Pilihan bahasa tersinkronisasi mulus dengan profil masing-masing pengguna untuk kenyamanan interaksi jangka panjang.

### 4. 📊 Studio Analitik Penggemar (Creator Insights)
*Dashboard* pengguna bukanlah sekadar kotak masuk biasa, tetapi **Studio Analitik** interaktif yang dibangun menggunakan `Chart.js`:
- **Tren Curhatan**: Kurva grafik jumlah pesan dalam 7 hari terakhir.
- **Distribusi Sentimen Emoji**: Melacak reaksi favorit pengirim dalam bagan *Doughnut*.
- **Radar Waktu Puncak**: Melihat jam aktif audiens untuk optimalisasi respons.
- **Sistem Perangkat**: Melacak proporsi sistem operasi pengunjung.

### 5. 🧨 Mode Rahasia Ekstra (Self-Destruct Messages)
Dilengkapi mode khusus "Pesan Bom Waktu" *(Disposable Message)*. Pesan jenis ini hanya bisa dibuka oleh penerima sebanyak **SATU KALI**, dan langsung terbakar (*deleted from database*) secara otomatis guna menjaga tingkat kerahasiaan paling maksimum ala agen mata-mata.

### 6. 🛡️ Tameng Anti-Spam Berlapis
- **Rate Limiting**: Kombinasi sistem limit internal (3 pesan per menit) untuk menendang *IP address* yang terlampau agresif.
- **Redis Throttling**: Akselerator *Backend* dan batas kecepatan di setiap aliran data transaksi/formulir sensitif.
- **Blocklist & IP Filter**: Penerima bisa langsung menekan tombol blokir pada pesan yang ditujukan padanya untuk membuang spesifik pengirim anonim ke zona daftar hitam.

### 7. 📸 Eksport IG Story Sepenuhnya
Melalui kolaborasi `html2canvas`, semua bentuk pesan bisa diabadikan dalam sekejap menjadi gambar indah yang mulus dan proporsional untuk diteruskan menjadi konten di berbagai media sosial, termasuk fitur semburan *Confetti* interaktif.

---

## 🛠️ Stack Teknologi (Tech Stack)

Arsitektur aplikasi dikombinasikan dengan berbagai spesifikasi *modern-framework*:

- **Backend Framework**: Python 3.12+, Django 6.0
- **Asynchronous Server**: Daphne & Django Channels *(WebSockets & ASGI API)*
- **Data & Caching**: SQLite / PostgreSQL, **Redis Server** (via `django-redis` & `channels-redis`)
- **Frontend / Styling**: Vanilla JavaScript, Bootstrap 5, Custom CSS Variables
- **Library Tambahan Web**: Chart.js, HTML2Canvas, AOS.js, Canvas-Confetti
- **Server Deployment (Production)**: Nginx Reverse Proxy & *Systemd Daemon* Middleware

---

## 🚀 Panduan Instalasi & Pengembangan di Lokal

Bagi pengembang yang ingin memeriksa atau mengembangkan lebih jauh aplikasi CurhatBox, silakan ikuti petunjuk berikut:

### Prasyarat (Prerequisites)
Pastikan sistem operasi Anda (Linux/Windows/macOS) telah dilengkapi oleh:
- **Python >= 3.10**
- **Sistem Redis Server** yang berjalan di _background_ (untuk kebutuhan Rate-limit & Caching)

### 1. Kloning Repositori & Persiapan Direktori
```bash
git clone https://github.com/Kemalhafizh/curhatbox.git
cd curhatbox
```

### 2. Lingkungan Virtual (Virtual Environment)
Isolasi semua kumpulan paket instalasi dengan venv:
```bash
python3 -m venv venv
source venv/bin/activate  # (Tulis `.\venv\Scripts\activate` jika memakai Windows)
```

### 3. Instalasi Dependensi Inti
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Variabel Lingkungan (`.env`)
Salin atau buat file `.env` di jalur terdepan direktori proyek Anda secara mandiri (karena file instalasi ini dilindungi oleh `.gitignore`).
```env
# SECURITY SETTINGS
SECRET_KEY=django-insecure-generate-secret-sendiri
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# EMAIL SETTINGS (SMTP)
DEFAULT_FROM_EMAIL=CurhatBox Admin <admin@domain-anda.com>
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.penyedialayanananda.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=admin@domain-anda.com
EMAIL_HOST_PASSWORD=kode_password_aplikasi_anda
```

### 5. Migrasi Skema Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Menjalankan *Asynchronous Development Server*
```bash
python manage.py runserver
```
🔥 Buka Web Browser Anda ke alamat `http://127.0.0.1:8000/`.

---

## 🔒 Laporan Standar Keamanan & Repositori

Proyek ini telah dikurasi dan diaudit sebelum repositori ini diterbitkan sebagai program sumber terbuka (*Open Source*):
- **Sistem Bersih (Cleaned Repository)**: `.env`, `db.sqlite3`, `media/` pengguna asli, dan rahasia log tidak pernah diterbitkan (berada di luar struktur GIT berkat pengerasan `.gitignore`).
- **Defleksi Serangan Lintas Situs**: Penerapan `{% csrf_token %}` keras yang absolut di ranah transaksi perubahan state sistem.

---

<p align="center" style="margin-top: 3rem;">
  <b>Didesain dan dikembangkan dengan ❤️ oleh Kemal Hafizh.</b><br/>
  <i>Edisi Penyempurnaan V-6.9.1 Tahun 2026.</i>
</p>