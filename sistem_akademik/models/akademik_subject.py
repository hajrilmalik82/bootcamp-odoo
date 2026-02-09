from odoo import models, fields

class AkademikSubject(models.Model):
    _name = 'akademik.subject'
    _description = 'Academic Subject'
    _rec_name = 'name'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    credits = fields.Integer(string='Credits', required=True)
    type = fields.Selection([
        ('compulsory', 'Compulsory'),
        ('elective', 'Elective')
    ], string='Type', required=True, default='compulsory')
