from odoo import models, fields, api

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Book Author'

    name = fields.Char('Author Name', required=True)
    
    # Relasi ke Buku (Inverse dari Many2many di buku)
    # butuh ini supaya Author 'sadar' dia nulis buku apa saja 
    book_ids = fields.Many2many('library.book', string='Books')
    # Computed Field: Menghitung jumlah buku
    book_count = fields.Integer('Book Count', compute='_compute_book_count')
    #Add a Weight (Number) field to the Author model.
    author_weight = fields.Integer('Author Weight', default=0)
    organization_id = fields.Many2one('library.organization', string='Organization')
    # SQL Constraint: Nama penulis tidak boleh kembar
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The author name must be unique!')
    ]

    @api.depends('book_ids')
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)