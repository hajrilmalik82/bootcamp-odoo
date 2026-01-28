from odoo import models, _, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            if not order.date_order:
                raise UserError(_("Isi Order Date terlebih dahulu."))

            # Info Tanggal Order
            o_date = order.date_order
            o_day = o_date.day
            o_month = o_date.month
            o_year = o_date.year

            # 1. Ambil Deadline Config
            deadline_rec = self.env["quota.deadline"].search([], limit=1)
            # Jika tidak ada config, default tanggal 25
            deadline_day = deadline_rec.deadline_day if deadline_rec else 25

            category_qty = {}
            for line in order.order_line:
                if line.display_type: continue
                product_tmpl = line.product_id.product_tmpl_id
                if not product_tmpl.quota_category_id:
                    continue
                
                qc = product_tmpl.quota_category_id
                category_qty.setdefault(qc, 0.0)
                category_qty[qc] += line.product_uom_qty

            # 3. Loop Validasi per Kategori
            for qc, requested_qty in category_qty.items():
                
                # A. VALIDASI GLOBAL (No. 1)
                allocation = self.env["quota.allocation"].search([
                    ("quota_category_id", "=", qc.id),
                    ("year", "=", o_year),
                ], limit=1)

                if allocation:
                    # Ambil baris alokasi untuk bulan ini
                    alloc_line = allocation.line_ids.filtered(lambda l: l.month == o_month)
                    
                    if alloc_line:
                        global_limit = alloc_line[0].quantity 

                        # HITUNG USAGE GLOBAL (Semua User)
                        # deadline_day=0 artinya: Hitung semua tanggal 1-31 (Global tidak kenal deadline)
                        used_global = self._get_usage(qc.id, o_year, o_month, deadline_day=0)

                        if (used_global + requested_qty) > global_limit:
                            raise UserError(_(
                                "GLOBAL QUOTA EXCEEDED\n"
                                "Category: %s\n"
                                "Limit: %s | Used: %s | Requested: %s\n"
                                "Remaining: %s"
                            ) % (qc.name, global_limit, used_global, requested_qty, (global_limit - used_global)))


                # B. VALIDASI CUSTOMER (No. 2 - Cek Deadline)
                # Hanya validasi jika tanggal order <= deadline
                if o_day <= deadline_day:
                    
                    customer_quota = self.env["customer.quota"].search([
                        ("partner_id", "=", order.partner_id.id),
                        ("quota_category_id", "=", qc.id),
                        ("year", "=", o_year),
                        ("month", "=", o_month),
                    ], limit=1)

                    if not customer_quota:
                        continue
                        # Jika settingan customer tidak ada, Error / lanjut
                        # raise UserError(_(
                        #     "Customer Quota belum disetting!\nCustomer: %s\nKategori: %s"
                        # ) % (order.partner_id.name, qc.name))

                    cust_limit = customer_quota.quantity
                
                    used_cust = self._get_usage(
                        qc.id, 
                        o_year, 
                        o_month, 
                        partner_id=order.partner_id.id, 
                        deadline_day=deadline_day
                    )

                    if (used_cust + requested_qty) > cust_limit:
                        raise UserError(_(
                            "CUSTOMER QUOTA EXCEEDED\n"
                            "Customer: %s\n"
                            "Limit: %s | Used Valid: %s | Requested: %s"
                        ) % (order.partner_id.name, cust_limit, used_cust, requested_qty))

        return super().action_confirm()
    def _get_usage(self, category_id, year, month, partner_id=False, deadline_day=0):
        """
        Menghitung total qty yang sudah confirm di database.
        
        Args:
            deadline_day (int): 
                - Jika 0: Hitung semua order di bulan itu (Logic Global).
                - Jika > 0: Hanya hitung order yang tanggalnya <= deadline_day (Logic Customer).
        """
        
        # 1. Buat Domain Dasar (Filter Awal)
        domain = [
            ('order_id.state', 'in', ['sale', 'done']),
            ('product_id.product_tmpl_id.quota_category_id', '=', category_id),
            ('order_id.id', '!=', self.id) 
        ]
        
        # Filter spesifik customer jika ada
        if partner_id:
            domain.append(('order_id.partner_id', '=', partner_id))
            
        # 2. Ambil semua Sales Order Line yang cocok
        all_lines = self.env['sale.order.line'].search(domain)
        
        total_used = 0.0
        
        # 3. Loop Python untuk Filter Tanggal secara Spesifik
        for line in all_lines:
            d = line.order_id.date_order
            if d and d.year == year and d.month == month:
                
                if deadline_day > 0 and d.day > deadline_day:
                    continue
                
                total_used += line.product_uom_qty
                    
        return total_used