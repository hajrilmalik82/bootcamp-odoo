from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Book Category'

    name = fields.Char('Category Name', required=True)

    # SQL Constraint: Mencegah nama kategori kembar di database
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The category name must be unique!')
    ]