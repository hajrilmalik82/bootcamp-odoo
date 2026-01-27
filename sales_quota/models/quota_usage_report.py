from odoo import models, fields

class QuotaUsageReport(models.Model):
    _name = "quota.usage.report"
    _description = "Quota Usage Report"
    _auto = False

    quota_category_id = fields.Many2one("quota.category", readonly=True)
    year = fields.Integer(readonly=True)
    month = fields.Integer(readonly=True)
    allocated_qty = fields.Float(readonly=True)
    used_qty = fields.Float(readonly=True)
    remaining_qty = fields.Float(readonly=True)

    def init(self):
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW quota_usage_report AS (
            SELECT
                row_number() OVER () AS id,
                qc.id AS quota_category_id,
                EXTRACT(YEAR FROM so.date_order)::int AS year,
                EXTRACT(MONTH FROM so.date_order)::int AS month,
                qal.quantity AS allocated_qty,
                SUM(sol.product_uom_qty) AS used_qty,
                qal.quantity - SUM(sol.product_uom_qty) AS remaining_qty
            FROM sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            JOIN quota_category qc ON pt.quota_category_id = qc.id
            JOIN quota_allocation qa ON qa.quota_category_id = qc.id
            JOIN quota_allocation_line qal ON qal.allocation_id = qa.id
            WHERE so.state IN ('sale', 'done')
              AND qa.year = EXTRACT(YEAR FROM so.date_order)
              AND qal.month = EXTRACT(MONTH FROM so.date_order)
            GROUP BY
                qc.id,
                EXTRACT(YEAR FROM so.date_order),
                EXTRACT(MONTH FROM so.date_order),
                qal.quantity
        )
    """)

