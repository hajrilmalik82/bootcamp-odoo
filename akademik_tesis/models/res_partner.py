from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    krs_ids = fields.One2many('akademik.krs', 'student_id', string='KRS')
