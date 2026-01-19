from odoo import models, fields, api

class LibraryOrganization(models.Model):
    _name = 'library.organization'
    _description = 'Library Organization'

    name = fields.Char('Organization Name', required=True)
    
    # Soal 5a: Bobot Organisasi
    org_weight = fields.Integer('Organization Weight', default=0)

    # Soal 5b: Daftar Buku (Computed Many2many)
    # Kenapa computed? Karena tidak ada kolom 'organization_id' di tabel Buku.
    # mencari buku secara manual lewat perantara Penulis.
    book_ids = fields.Many2many(
        'library.book', 
        string='Books', 
        compute='_compute_book_ids'
    )

    def _compute_book_ids(self):
        for org in self:
            # 1. mencari siapa saja penulis yang gabung di organisasi ini
            authors = self.env['library.author'].search([('organization_id', '=', org.id)])
            
            # 2. mengambil semua buku milik penulis-penulis tersebut
            # .mapped('book_ids') cara cepat mengambil field dari banyak record sekaligus
            org.book_ids = authors.mapped('book_ids')