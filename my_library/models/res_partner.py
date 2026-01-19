from odoo import models, fields

class ResPartner(models.Model):
    # TEKNIK: INHERITANCE
    #  memberitahu Odoo: "Pinjam model 'res.partner' (Contacts), lalu tambahkan field di bawah ini ke sana."
    _inherit = 'res.partner'
    
    
    # TEKNIK: BASIC FIELDS
    # Menambah kolom baru ke tabel res_partner
    
    # --- Challenge No 2: Add Sponsor Status (Yes/No) ---
    # Field Boolean otomatis jadi kotak centang (Checkbox)
    is_sponsor = fields.Boolean("Sponsor Status") 

    # --- Challenge No 2: Add Weight (Number) ---
    # Field Integer untuk menyimpan angka bulat
    sponsor_weight = fields.Integer("Sponsor Weight")