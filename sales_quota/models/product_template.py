from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    quota_category_id = fields.Many2one(
        "quota.category",
        string="Quota Category"
    )
