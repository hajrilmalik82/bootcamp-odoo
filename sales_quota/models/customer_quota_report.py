from odoo import models, fields, tools

class CustomerQuotaReport(models.Model):
    _name = "customer.quota.report"
    _description = "Customer Quota Usage Report"
    _auto = False
    _rec_name = 'partner_id'
    _order = 'year desc, month desc'

    # Identitas
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    quota_category_id = fields.Many2one("quota.category", string="Category", readonly=True)
    year = fields.Integer(string="Year", readonly=True)
    month = fields.Integer(string="Month", readonly=True)
    
    # Kolom Angka (Limit, Used, Remaining)
    limit_qty = fields.Float(string="Limit Quantity", readonly=True)
    used_qty = fields.Float(string="Used Quantity", readonly=True)
    remaining_qty = fields.Float(string="Remaining Quantity", readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW customer_quota_report AS (
                SELECT
                    row_number() OVER() AS id,
                    cq.id AS customer_quota_id,
                    cq.partner_id,
                    cq.quota_category_id,
                    cq.year,
                    cq.month,
                    
                    -- 1. LIMIT (Ambil dari tabel customer_quota)
                    cq.quantity AS limit_qty,
                    
                    -- 2. USED (Hitung dari Sales Order Line yang VALID saja)
                    COALESCE(sales.qty, 0) AS used_qty,
                    
                    -- 3. REMAINING (Limit - Used)
                    (cq.quantity - COALESCE(sales.qty, 0)) AS remaining_qty

                FROM customer_quota cq
                
                -- LEFT JOIN Data Penjualan per Customer
                LEFT JOIN (
                    SELECT
                        so.partner_id,
                        pt.quota_category_id,
                        EXTRACT(YEAR FROM so.date_order)::int AS so_year,
                        EXTRACT(MONTH FROM so.date_order)::int AS so_month,
                        SUM(sol.product_uom_qty) AS qty
                    FROM sale_order_line sol
                    JOIN sale_order so ON sol.order_id = so.id
                    JOIN product_product pp ON sol.product_id = pp.id
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    WHERE so.state IN ('sale', 'done')
                    
                      AND EXTRACT(DAY FROM so.date_order) <= (
                          SELECT COALESCE(MAX(deadline_day), 25) FROM quota_deadline
                      )

                    GROUP BY 
                        so.partner_id,
                        pt.quota_category_id,
                        EXTRACT(YEAR FROM so.date_order),
                        EXTRACT(MONTH FROM so.date_order)
                ) sales 
                ON 
                    sales.partner_id = cq.partner_id AND
                    sales.quota_category_id = cq.quota_category_id AND
                    sales.so_year = cq.year AND
                    sales.so_month = cq.month
            )
        """)