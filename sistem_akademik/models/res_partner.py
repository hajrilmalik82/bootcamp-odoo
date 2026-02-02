from odoo import models, fields, api
import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    identitas_mahasiswa = fields.Boolean(string='Identitas Mahasiswa')
    nim = fields.Char(string='NIM')
    prodi_id = fields.Many2one('akademik.prodi', string='Program Studi')
    jenjang = fields.Selection([
        ('s1', 'S1'),
        ('pasca', 'Pasca')
    ], string='Jenjang')
    level_prestasi = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ], string='Level Prestasi')
    tag_mahasiswa = fields.Many2many(
        'res.partner.category',
        'mahasiswa_tag_rel',
        string='Tag Mahasiswa'
    )
    tahun_masuk = fields.Many2one('akademik.tahun', string='Tahun Masuk')
    topik_riset = fields.Char(string='Topik Riset')
    dosen_pembimbing_id = fields.Many2one('res.partner', string='Dosen Pembimbing')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('aktif', 'Aktif'),
        ('lulus', 'Lulus'),
        ('dropout', 'Drop Out')
    ], string='Status Mahasiswa', default='draft')

    def action_generate_nim(self):
        for record in self:
            if not record.nim:
                year = datetime.datetime.now().year
                record.nim = f"{year}{record.id or '0000'}"

    @api.depends('name', 'nim', 'identitas_mahasiswa')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()
        for record in self:
            if record.nim:
                record.display_name = f"[{record.nim}] {record.name}"
