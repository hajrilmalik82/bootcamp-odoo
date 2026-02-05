from odoo import models, fields, api

class AkademikTesis(models.Model):
    _name = 'akademik.tesis'
    _description = 'Akademik Tesis'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Judul Tesis', required=True)
    mahasiswa_id = fields.Many2one(
        'res.partner', 
        string='Mahasiswa', 
        domain=[('identitas_mahasiswa', '=', True)],
        required=True
    )
    pembimbing_id = fields.Many2one(
        'hr.employee', 
        string='Pembimbing', 
        domain=[('is_dosen', '=', True)]
    )
    tanggal_pengajuan = fields.Date(string='Tanggal Pengajuan', default=fields.Date.today)
    progress = fields.Integer(string='Persentase Selesai')
    progress_kategori = fields.Selection([
        ('low', 'Rendah (0-49%)'),
        ('medium', 'Sedang (50-99%)'),
        ('high', 'Tinggi (100%)')
    ], compute='_compute_progress_kategori', string='Kategori Progress')

    @api.depends('progress')
    def _compute_progress_kategori(self):
        for record in self:
            if record.progress == 100:
                record.progress_kategori = 'high'
            elif record.progress >= 50:
                record.progress_kategori = 'medium'
            else:
                record.progress_kategori = 'low'

    tahapan = fields.Selection([
        ('pengajuan_judul', 'Pengajuan Judul'),
        ('penunjukan_pembimbing', 'Penunjukan Pembimbing'),
        ('seminar_proposal', 'Seminar Proposal'),
        ('penelitian', 'Penelitian'),
        ('sidang_akhir', 'Sidang Akhir'),
        ('yudisium', 'Yudisium')
    ], string='Tahapan', default='pengajuan_judul', group_expand='_expand_tahapan')

    @api.model
    def _expand_tahapan(self, states, domain, order):
        return [key for key, val in type(self).tahapan.selection]
