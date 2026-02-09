from odoo import models, fields, api

class AkademikThesisDocument(models.Model):
    _name = 'akademik.tesis.dokumen'
    _description = 'Thesis Document'

    name = fields.Char(string='Document Name', required=True)
    file = fields.Binary(string='File', required=True, attachment=True)
    file_name = fields.Char(string='File Name')
    type = fields.Selection([
        ('title_submission', 'Title Submission'),
        ('proposal', 'Proposal'),
        ('research', 'Research'),
        ('final_report', 'Final Report')
    ], string='Document Type', required=True)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_verified', 'To be Verified'),
        ('verified', 'Verified')
    ], string='Status', default='draft', required=True)
    
    thesis_id = fields.Many2one('akademik.tesis', string='Thesis', ondelete='cascade')

    def action_submit(self):
        for record in self:
            record.status = 'to_be_verified'

    def action_verify(self):
        for record in self:
            record.status = 'verified'
