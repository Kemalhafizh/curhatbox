<div align="center">
  <img src="https://img.icons8.com/clouds/200/mailbox-closed-flag-up.png" alt="CurhatBox Logo" width="150"/>
  <h1>💜 CurhatBox v7.0 (Enterprise Edition)</h1>
  <p><strong>Platform Pesan Anonim Premium Berkualitas SaaS dengan Keamanan Anti-Spam Tingkat Lanjut & QA Automation</strong></p>
  
  <p>
    <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 6.0" />
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
    <img src="https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis Memory" />
    <img src="https://img.shields.io/badge/PostgreSQL-Data-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Bootstrap-5.3-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
    <img src="https://img.shields.io/badge/Test_Coverage-100%25-success?style=for-the-badge&logo=pytest&logoColor=white" alt="Testing" />
  </p>
</div>

---

## 📖 Apa itu CurhatBox?

**CurhatBox** adalah platform pengiriman pesan rahasia secara anonim (seperti NGL atau Secreto) namun diarsiteki ulang menggunakan standar *Enterprise* tahun 2026. Dibangun di atas fondasi **Django 6.0 Asynchronous (Daphne)**, platform ini super interaktif, mulus, dan sangat tangguh terhadap ancaman keamanan dan *spam*.

Dengan antarmuka mengadopsi tren **Glassmorphism**, CurhatBox tidak hanya alat main-main untuk *Instagram Story*, tapi merupakan pondasi proyek *SaaS (Software as a Service)* yang siap ditarungkan di level skala besar.

---

## ✨ Fitur-Fitur Premium (Key Features)

### 1. 🎨 Modern SaaS UI/UX (Glassmorphism & Animasi)
- **Fluid UI**: Desain kristal tembus pandang (Glassmorphism) berpadu dengan *Liquid Gradients*.
- **Asynchronous Animations**: Menggunakan **AOS (Animate On Scroll)** untuk pengalaman navigasi tanpa jeda.
- **Premium Error Catching**: Jika *user* tersesat (404), salah akses (403), atau server sedang kewalahan (500), website akan menampilkan animasi ramah pengguna dan tidak akan pernah menampilkan kode *error* mentah yang membingungkan.

### 2. 🔐 Keamanan & Autentikasi Kelas Atas
- **Password Reset via Email TLS**: Dilengkapi SMTP ganti sandi otomatis layaknya aplikasi modern.
- **Smart Cooldown**: Batasan pendaftaran ulang dan batas pengiriman OTP dikendalikan secara mutlak menggunakan durasi *In-Memory* di **Redis**.

### 3. 🛡️ Tameng Anti-Spam & QA Automaton
- **Automated Virtual QA**: Website dibekali 16 skenario bot penguji (Unit Tests) berbasis memori lokal (SQLite-Memory). Modifikasi kode di masa depan dijamin bebas dari kutu (Regresi).
- **Censor Filter API**: Robot penyensor kata kasar cerdas buatan yang kebal dari tulisan alay atau kombinasi tanda baca (Contoh: `t0L0L` atau `4nJ|ng` otomatis dibumihanguskan).
- **IP Blocklist & Auto Rate-Limit**: Sistem akan meledakkan status "403 Forbidden" jika mendeteksi ada IP *(Internet Protocol)* spesifik yang mencoba mengirim 3 pesan lebih dalam satu menit. Sistem pemblokiran mutlak satu arah (User bisa Ban IP anonim!).

### 4. 📊 Creator Studio Analytics
Dashboard Anda bukanlah sekadar daftar baca masuk, tapi **Studio Analitik** interaktif ditenagai oleh `Chart.js`:
- Curva lalu lintas tren curhatan mingguan.
- Diagram kue (Doughnut) radar distribusi emoji atau sentimen curhatan.
- Pelacakan jenis Perangkat & Browser milik sang pengirim pesan anonim.

### 5. 📸 One-Click IG Story Export
Tinggalkan fitur tangkapan layar! CurhatBox terintegrasi dengan **html2canvas** yang secara gaib mencetak pesan anonim jadi ilustrasi gambar resolusi tinggi berdampingan dengan hujan *Confetti* siap masuk profil sosial media.

### 6. 🌐 Global Multilingual (i18n)
Sistem adaptif terjemahan (Inggris & Indonesia). Sistem secara otomatis membaca kebiasaan peramban lokal dan menyediakan *Language Switcher* mewah di dasar layar.

### 7. ⏱️ Disposable Messages (Pesan Bom Waktu)
Pesan rahasia yang bersifat sakral bisa diaktifkan mode agen rahasianya. Hanya bisa diintip dan dibaca satu detik oleh penerima, lalu datanya akan terbakar dan meledak hilang (**Cascade Delete**) dari ruang Database untuk selamanya.

---

## 🛠️ Stack Teknologi (Architecture)

- **Backend Logic**: Python 3.12+, Django 6.0
- **Asynchronous Bridge**: Daphne ASGI, Django Channels
- **In-Memory Caching (Data Cepat)**: Redis Server (`django-redis`)
- **Primary Relational Database**: PostgreSQL (Production) / SQLite3 (Testing)
- **Frontend Core**: HTML5 Semantic, JS (ES6+), Bootstrap 5.3 Custom
- **Micro-Libraries**: Chart.js, HTML2Canvas, AOS.js, Confetti.

---

## 🚀 Panduan Instalasi (Development Setup)

Ingin ikut berkontribusi membangun CurhatBox di komputer lokal Anda? Ikuti langkah mudah ini:

### 1. Kloning & Buat Ruang Isolasi (Virtual Env)
```bash
git clone https://github.com/Kemalhafizh/curhatbox.git
cd curhatbox
python3 -m venv venv
source venv/bin/activate  # (Gunakan `.\venv\Scripts\activate` untuk pengguna Windows)
```

### 2. Panggil Semua Tenaga (Install Requirements)
```bash
pip install -r requirements.txt
```

### 3. Setup Kunci Rahasia Anda (.env)
Bikin satu file bernama `.env` (tanpa huruf besar di awal) dan isi kerahasiaannya:
```env
# Keamanan Inti Server
SECRET_KEY=isi-kode-unik-acak-anda-disini
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Eksternal (Opsional untuk fitur reset sandi)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=email.kamu@gmail.com
EMAIL_HOST_PASSWORD=kode_rahasia_aplikasi_gmail_kamu
```

### 4. Bangun Database & Uji Coba Kesehatannya
```bash
python manage.py migrate
# Uji coba kekuatan pertahanan aplikasi dengan sistem robot QA kita!
python manage.py test main --settings=curhatbox.test_settings
```

### 5. Luncurkan Satelit Server
```bash
python manage.py runserver
```
🔥 Buka Web Browser Anda ke alamat `http://127.0.0.1:8000/`.

---

## 🔒 Laporan Standar Operasional Produksi

- Repositori disucikan menggunakan tembok tebal `.gitignore` tingkat lanjut untuk menghalangi masuknya data kunci ke publik.
- **CSRF Tokens Middleware** dipatenkan secara permanen pada setiap alur transaksi (Data mutlak kebal dari serangan silang *Cross-Site Request Forgery*).
- Form Input dieksekusi secara ketat mencegah injeksi kode (*Cross Site Scripting / XSS*).

<br>
<p align="center">
  <b>Direkayasa dan dikembangkan dengan ❤️ oleh Kemal Hafizh.</b><br/>
  <i>Edisi Penyempurnaan V-7.0 (Enterprise) Tahun 2026.</i>
</p>