from odoo import models, fields

class QuotaCategory(models.Model):
    _name = "quota.category"
    _description = "Quota Category"

    name = fields.Char(required=True)
    