# EnglishKids LMS

**EnglishKids LMS** adalah platform Learning Management System (LMS) modern berbasis Django, dirancang khusus untuk membantu anak-anak belajar bahasa Inggris secara online dengan fitur tugas, kuis, dan pemantauan progres yang interaktif.

---

## ✨ Fitur Utama

- **Manajemen Tugas (Homework)**

  - Lihat, kerjakan, dan kumpulkan tugas (catatan atau kuis) secara online.
  - Status tugas: Sudah dikerjakan, menunggu persetujuan, atau belum dikerjakan.
  - Upload gambar untuk tugas catatan.

- **Kuis Interaktif**

  - Siswa dapat mengerjakan kuis yang disiapkan guru.
  - Hasil kuis langsung terekam di sistem.

- **Manajemen Kelas & Kursus**

  - Guru dapat membuat kursus dan materi pelajaran.
  - Siswa dapat melihat daftar kursus dan materi yang tersedia.

- **Dashboard Siswa & Guru**

  - Tampilan dashboard berbeda untuk siswa dan guru.
  - Guru dapat memantau progres siswa dan menyetujui tugas.

- **Autentikasi & Role**

  - Sistem login, logout, dan profile.
  - Role: Siswa dan Guru.

- **Admin Panel**

  - Kelola user, tugas, kursus, dan approval tugas dari admin Django.

- **UI Modern & Responsif**
  - Tampilan bersih, ramah anak, dan mobile-friendly.

---

## 🚀 Instalasi & Setup

1. **Clone repository**

   ```bash
   git clone https://github.com/username/englishkids-lms.git
   cd englishkids-lms
   ```

2. **Buat virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # atau venv\Scripts\activate di Windows
   pip install django mysqlclient
   ```

3. **Konfigurasi database**

   - Edit `lms_project/settings.py` bagian `DATABASES` sesuai database MySQL kamu.

4. **Migrasi database**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Buat superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Jalankan server**

   ```bash
   python manage.py runserver
   ```

7. **Akses di browser**
   - Buka [http://localhost:8000](http://localhost:8000)

---

## 🗂️ Struktur Project

- `users/` : Manajemen user, autentikasi, dan profile.
- `courses/` : Manajemen kursus, materi, dan hasil kuis.
- `homework/` : Manajemen tugas, pengumpulan, dan approval.
- `templates/` : Template HTML untuk semua halaman.
- `static/` : File CSS, JS, dan gambar statis.

---

## 🧑‍💻 Fitur Teknis

- **Custom User Model** dengan role (student/teacher)
- **Homework & Submission**: Tugas bisa berupa catatan (upload gambar) atau quiz
- **Approval System**: Guru/admin bisa menyetujui tugas siswa
- **Quiz Result Tracking**: Nilai dan progres kuis terekam otomatis
- **Responsive UI**: Desain modern, cocok untuk anak-anak

---

## 📸 Preview

> Tambahkan screenshot halaman utama, dashboard, dan tugas di sini!

---

## 🤝 Kontribusi

Pull request dan issue sangat terbuka untuk pengembangan lebih lanjut!

---

## 📄 Lisensi

MIT License

---

**EnglishKids LMS** – Belajar Bahasa Inggris jadi lebih seru dan terstruktur! 🚀
