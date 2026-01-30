from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    quota_remaining_info = fields.Integer(
        string="Remaining Quota",
        compute="_compute_quota_remaining_info",
        store=False,
        readonly=True
    )

    @api.depends('product_id', 'product_uom_qty', 'order_id.partner_id', 'order_id.date_order', 'order_id.state', 'order_id.order_line.product_uom_qty', 'order_id.order_line.product_id')
    def _compute_quota_remaining_info(self):
        for line in self:
            remaining = 0
            if line.product_id and line.order_id.partner_id and line.order_id.date_order:
                # 1. Cek Kategori Produk
                product_tmpl = line.product_id.product_tmpl_id
                qc = product_tmpl.quota_category_id
                
                if qc:
                    # 2. Ambil Info Tanggal
                    o_date = line.order_id.date_order
                    o_year = o_date.year
                    o_month = o_date.month
                    
                    # 3. limit Customer
                    customer_quota = self.env["customer.quota"].search([
                        ("partner_id", "=", line.order_id.partner_id.id),
                        ("quota_category_id", "=", qc.id),
                        ("year", "=", o_year),
                        ("month", "=", o_month),
                    ], limit=1)
                    
                    limit = customer_quota.quantity if customer_quota else 0.0

                    used_other = line.order_id._get_usage(qc.id, o_year, o_month, partner_id=line.order_id.partner_id.id)
                    
                    current_order_usage = 0.0
                    for l in line.order_id.order_line:
                        if l.product_id.product_tmpl_id.quota_category_id == qc:
                            current_order_usage += l.product_uom_qty
                            
                    # Total Terpakai = Punya Orang Lain + Order Ini
                    total_used = used_other + current_order_usage
                    remaining = int(limit - total_used)
            
            line.quota_remaining_info = remaining

    @api.constrains('product_uom_qty', 'product_id')
    def _check_quota_limit_on_edit(self):
        for line in self:
            if line.order_id.state in ['sale', 'done']:
                
                product_tmpl = line.product_id.product_tmpl_id
                qc = product_tmpl.quota_category_id
                if not qc: continue
                
                o_date = line.order_id.date_order
                o_year = o_date.year
                o_month = o_date.month
                
                customer_quota = self.env["customer.quota"].search([
                    ("partner_id", "=", line.order_id.partner_id.id),
                    ("quota_category_id", "=", qc.id),
                    ("year", "=", o_year),
                    ("month", "=", o_month),
                ], limit=1)
                limit = customer_quota.quantity if customer_quota else 0.0
                
                used_other = line.order_id._get_usage(qc.id, o_year, o_month, partner_id=line.order_id.partner_id.id)
                
                current_order_usage = 0.0
                for l in line.order_id.order_line:
                    if l.product_id.product_tmpl_id.quota_category_id == qc:
                        current_order_usage += l.product_uom_qty
                
                total_used = used_other + current_order_usage
                
                if total_used > limit:
                     raise ValidationError(_(
                        "BLOKIR EDIT: Quota Jebol!\n"
                        "Anda mencoba mengubah qty order yang sudah confirm.\n"
                        "Total Request: %s | Limit: %s\n"
                        "Mohon kurangi qty atau minta tambahan kuota."
                    ) % (total_used, limit))
