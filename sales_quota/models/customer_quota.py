from odoo import models, fields

class CustomerQuota(models.Model):
    _name = "customer.quota"
    _description = "Customer Quota"

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True
    )

    quota_category_id = fields.Many2one(
        "quota.category",
        string="Quota Category",
        required=True
    )

    year = fields.Integer(required=True)
    month = fields.Integer(required=True)

    quantity = fields.Float(
        string="Remaining Quantity",
        required=True
    )
