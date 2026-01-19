from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    # --- FIELD DEFINITIONS ---
    name = fields.Char('Title', required=True)
    category_id = fields.Many2one('library.category', string='Category')
    publication_year = fields.Integer('Publication Year')
    
    # Relasi ke Penulis (Many2many)
    author_ids = fields.Many2many('library.author', string='Authors')
    
    # Relasi ke Sponsor (Many2one)
    # Domain: Hanya tampilkan contact yang field 'is_sponsor'-nya True
    # dari model book ke filed sponsor yang diambil dari tabel partner
    sponsor_id = fields.Many2one(
        'res.partner', 
        string='Sponsor', 
        domain="[('is_sponsor', '=', True)]"
    )

    # NO 3: BASIC SCORE
    # Definisi Field untuk menampung hasil hitungan
    basic_score = fields.Float(
        string='Basic Score',          # Label yang muncul di layar
        compute='_compute_basic_score',# Nama fungsi yang akan menghitung nilainya
        store=True,                    # Simpan hasil hitungan di database (agar bisa disortir/filter)
        readonly=True                  # tidak boleh edit manual
    )
    
    # --- CHALLENGE NO 4b: FINAL SCORE (SUM OF WEIGHTS ---
    final_score = fields.Float(
        string='Final Score',           # Label di layar
        compute='_compute_final_score', # Nama fungsi penghitungnya
        store=True,                     # Simpan hasil di database
        readonly=True                   # User tidak bisa edit manual (harus otomatis)
    )
    # harus hitung ulang jika
    # 1. Saat 'publication_year' berubah.
    # 2. Saat 'sponsor_weight' milik 'sponsor_id' berubah.
    @api.depends('publication_year', 'sponsor_id.sponsor_weight')
    def _compute_basic_score(self):
        # Looping 'self'
        # Sangat PENTING di Odoo. 'self' bisa berisi 1 buku atau 1000 buku sekaligus.
        # Kita harus loop satu per satu agar perhitungan aman saat edit massal.
        for book in self:
            
            # Inisialisasi skor awal
            # Kita mulai dari 0 untuk setiap buku yang sedang di-loop
            score = 0
            
            # --- LOGIKA A: POIN TAHUN TERBIT ---
            
            # Cek apakah tahun diisi? 
            # (Jika kosong, lewati logika tahun agar tidak error)
            if book.publication_year:
                
                if book.publication_year < 2000:
                    score += 5  # Tambah 5 poin ke variabel score
                # Jika tahun antara 2000 sampai 2019 (inklusif)
                elif 2000 <= book.publication_year <= 2019:
                    score += 10 # Tambah 10 poin
                elif book.publication_year >= 2020:
                    score += 15 # Tambah 15 poin
            
            # --- LOGIKA B: POIN SPONSOR ---
            
            # Cek apakah buku punya sponsor?
            # Kita akses field relasi 'sponsor_id'
            if book.sponsor_id:
                
                # Ambil nilai 'sponsor_weight' dari tabel partner lewat relasi
                # Kalikan 0.5 (sama dengan 50%)
                bonus_sponsor = book.sponsor_id.sponsor_weight * 0.5
                
                # Tambahkan bonus sponsor ke skor total
                score += bonus_sponsor
            
            # 12. PENTING: Set nilai akhir ke field database
            # Masukkan total 'score' ke field 'basic_score' milik buku tersebut
            book.basic_score = score
        
     
    # COMPUTE FINAL SCORE (CHALLENGE NO 5)
    # hitung ulang jika
    # 1. Jika Basic Score berubah
    # 2. Jika Bobot Penulis berubah
    # 3. Jika Bobot Organisasi (milik penulis) berubah
    @api.depends('basic_score', 'author_ids.author_weight', 'author_ids.organization_id.org_weight')
    def _compute_final_score(self):
        for book in self:
            # 1. Ambil modal awal dari Basic Score
            total_akhir = book.basic_score
            
            # 2. Loop semua penulis di buku ini
            for author in book.author_ids:
                
                # Tambah bobot si penulis (Challenge 4)
                total_akhir += author.author_weight
                
                # Tambah bobot organisasi si penulis (Challenge 5c)
                # Cek dulu apakah penulis punya organisasi?
                if author.organization_id:
                    total_akhir += author.organization_id.org_weight
            
            # Simpan hasil akhir
            book.final_score = total_akhir
            
    # --- VALIDASI TAHUN ---
    @api.constrains('publication_year')
    def _check_publication_year(self):
        for record in self:
            if record.publication_year < 1990:
                raise ValidationError('Publication year must be after 1990.')