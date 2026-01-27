from odoo import models, fields

class QuotaAllocation(models.Model):
    _name = "quota.allocation"
    _description = "Quota Allocation"

    quota_category_id = fields.Many2one(
        "quota.category",
        required=True
    )

    year = fields.Integer(required=True)

    line_ids = fields.One2many(
        "quota.allocation.line",
        "allocation_id",
        string="Monthly Quotas"
    )


class QuotaAllocationLine(models.Model):
    _name = "quota.allocation.line"
    _description = "Quota Allocation Line"

    allocation_id = fields.Many2one(
        "quota.allocation",
        required=True,
        ondelete="cascade"
    )

    month = fields.Integer(required=True)
    quantity = fields.Float(
        string="Quantity",
        required=True
    )
