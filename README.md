<div align="center">

# 🚀 Bootcamp Odoo — Portfolio & Learning Journal

![Odoo](https://img.shields.io/badge/Odoo-17%20Community-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![OWL](https://img.shields.io/badge/OWL-Odoo%20Web%20Library-FF6B35?style=for-the-badge)

**Kumpulan modul custom Odoo 17** yang dibangun selama proses pembelajaran & bootcamp.  
Mencakup domain: Perpustakaan, Hostel, Sales, Akademik, hingga OWL Framework.

</div>

---

## 📦 Daftar Modul

| No | Modul | Domain | Deskripsi Singkat |
|----|-------|--------|-------------------|
| 1 | `my_library` | 📚 Library | Manajemen buku, kategori, peminjaman, dan anggota perpustakaan |
| 2 | `my_hostel` | 🏨 Hostel | Manajemen kamar, tamu, check-in/out, dan fasilitas asrama |
| 3 | `my_hostel_terminate` | 🏨 Hostel Extension | Tambahan fitur terminasi kontrak dan refund untuk hostel |
| 4 | `sales_quota` | 💼 Sales | Target kuota penjualan per sales representative |
| 5 | `sistem_akademik` | 🎓 Academic | Sistem KRS, jadwal kuliah, nilai, dan tesis perguruan tinggi |
| 6 | `learning_owl` | 🦉 OWL Framework | Eksplorasi & implementasi OWL (Odoo Web Library) |

---

## 🎓 Academic Management System (`sistem_akademik`)

Modul unggulan dalam portfolio ini — membangun sistem informasi akademik ( SIAKAD) lengkap.

### Fitur Utama
- ✅ **Manajemen Mahasiswa** — Data lengkap: NIM, Prodi, Angkatan, Status
- ✅ **KRS (Kartu Rencana Studi)** — Pendaftaran mata kuliah dengan validasi kapasitas ruangan
- ✅ **Jadwal Kuliah** — Penjadwalan kelas, klaim jadwal oleh dosen
- ✅ **Penilaian** — Input nilai oleh dosen, generate KHS
- ✅ **Tesis** — Pengajuan, bimbingan, approval skripsi
- ✅ **Role-based Access** — Officer, Dosen, Mahasiswa dengan hak akses berbeda

### Role & Access
| Role | Akses |
|------|-------|
| 🛠️ Officer | Full CRUD semua data |
| 👨‍🏫 Dosen | Lihat Mahasiswa bimbingan, Klaim Jadwal, Input Nilai |
| 🎓 Mahasiswa | Lihat KRS & Jadwal prodi sendiri |

---

## 🦉 OWL Framework (`learning_owl`)

Eksplorasi mendalam Odoo Web Library (OWL) — JavaScript framework official Odoo.

### Konsep yang Dipelajari
```
✅ useState & Reactive State    ✅ Props & Callback (Parent ↔ Child)
✅ ORM Service (searchRead)     ✅ CRUD Operations (create/write/unlink)
✅ Action & Dialog Service      ✅ Custom Field Widgets
✅ Lifecycle Hooks (onMounted)  ✅ Slots & Component Composition
```

---

## 🗃️ Stack Teknologi

```
Platform    : Odoo 17 Community Edition
Language    : Python 3.11 + XML + JavaScript (OWL)
Database    : PostgreSQL 14
ORM         : Odoo ORM (Models, Fields, API Decorators)
Frontend    : OWL (Odoo Web Library)
Security    : Record Rules + Access Control Lists (ACL)
```

---

## 🚀 Cara Instalasi

```bash
# 1. Clone repo ini ke folder addons
git clone https://github.com/hajrilmalik82/bootcamp-odoo.git

# 2. Tambahkan path ke odoo.conf
addons_path = /path/to/odoo/addons,/path/to/bootcamp-odoo

# 3. Install modul yang diinginkan via Settings > Apps
```

---

## 👤 Author

| | |
|--|--|
| **Nama** | Hajril Malik |
| **Platform** | Odoo 17 Community |
| **Focus** | Odoo Backend Development · OWL Frontend · Custom Module |
| **GitHub** | [@hajrilmalik82](https://github.com/hajrilmalik82) |

---

<div align="center">

*Dibangun dengan ❤️ selama perjalanan belajar Odoo Development*

</div>
