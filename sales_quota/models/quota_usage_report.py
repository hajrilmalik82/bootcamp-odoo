from odoo import models, fields, tools

class QuotaUsageReport(models.Model):
    _name = "quota.usage.report"
    _description = "Quota Usage Report"
    _auto = False
    _rec_name = 'quota_category_id'
    _order = 'year desc, month desc'

    quota_category_id = fields.Many2one("quota.category", readonly=True)
    year = fields.Integer(readonly=True)
    month = fields.Integer(readonly=True)
    
    # Kolom Angka
    allocated_qty = fields.Float(string="Limit", readonly=True)
    used_qty = fields.Float(string="Used", readonly=True)
    remaining_qty = fields.Float(string="Remaining", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW quota_usage_report AS (
                SELECT
                    row_number() OVER() AS id,
                    qal.id AS allocation_line_id,
                    qa.quota_category_id,
                    qa.year,
                    qal.month,
                    qal.quantity AS allocated_qty,
                    COALESCE(sales.qty, 0) AS used_qty,
                    (qal.quantity - COALESCE(sales.qty, 0)) AS remaining_qty
                FROM quota_allocation_line qal
                JOIN quota_allocation qa ON qal.allocation_id = qa.id
                LEFT JOIN (
                    SELECT
                        pt.quota_category_id,
                        EXTRACT(YEAR FROM so.date_order)::int AS so_year,
                        EXTRACT(MONTH FROM so.date_order)::int AS so_month,
                        SUM(sol.product_uom_qty) AS qty
                    FROM sale_order_line sol
                    JOIN sale_order so ON sol.order_id = so.id
                    JOIN product_product pp ON sol.product_id = pp.id
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    WHERE so.state IN ('sale', 'done')
                    GROUP BY pt.quota_category_id, EXTRACT(YEAR FROM so.date_order), EXTRACT(MONTH FROM so.date_order)
                ) sales ON sales.quota_category_id = qa.quota_category_id 
                       AND sales.so_year = qa.year 
                       AND sales.so_month = qal.month
            )
        """)