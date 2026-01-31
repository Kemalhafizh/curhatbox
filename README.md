# 💜 CurhatBox

**CurhatBox** adalah platform pengiriman pesan anonim (rahasia) yang aman dan privat. Dibangun menggunakan Django Framework, aplikasi ini memungkinkan pengguna menerima pesan jujur tanpa mengetahui identitas pengirim, lengkap dengan fitur integrasi ke Instagram Story.

## 🚀 Fitur Unggulan

* **100% Anonim:** Identitas pengirim dilindungi (hanya log IP yang disimpan untuk keamanan).
* **IG Story Generator:** Ubah pesan masuk menjadi gambar estetik siap posting ke Instagram Story.
* **Dashboard User:** Kelola pesan masuk, balas pesan, atau hapus pesan.
* **Sistem Blokir:** Blokir pengirim yang mengganggu berdasarkan IP Address.
* **Sensor Kata:** Otomatis menyensor kata-kata kasar/toksik.
* **Keamanan:** Password terenkripsi (PBKDF2) dan perlindungan CSRF & SQL Injection bawaan Django.

## 🛠️ Teknologi yang Digunakan

* **Backend:** Python, Django 6.0
* **Database:** SQLite (Dev) / PostgreSQL (Prod)
* **Frontend:** HTML5, Bootstrap 5, CSS3
* **Tools:** HTML2Canvas (untuk fitur IG Story)

## 📦 Cara Menjalankan di Local

Ingin mencoba menjalankannya di laptopmu? Ikuti langkah ini:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/Kemalhafizh/curhatbox.git](https://github.com/Kemalhafizh/curhatbox.git)
    cd curhatbox
    ```

2.  **Buat Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Migrasi Database**
    ```bash
    python manage.py migrate
    ```

5.  **Jalankan Server**
    ```bash
    python manage.py runserver
    ```

Buka browser dan akses: `http://127.0.0.1:8000/`

---
Dibuat dengan ❤️ oleh **Kemal Hafizh**.