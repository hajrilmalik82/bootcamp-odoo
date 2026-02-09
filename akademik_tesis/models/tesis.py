from odoo import models, fields, api

class AkademikThesis(models.Model):
    _name = 'akademik.tesis'
    _description = 'Academic Thesis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    title = fields.Char(string='Thesis Title', required=True)
    student_id = fields.Many2one(
        'res.partner', 
        string='Student', 
        domain="[('identitas_mahasiswa', '=', True), ('krs_ids.line_ids.subject_id.name', 'ilike', 'Tesis')]",
        required=True
    )
    supervisor_id = fields.Many2one(
        'hr.employee', 
        string='Supervisor', 
        domain="[('is_dosen', '=', True)]"
    )
    submission_date = fields.Date(string='Submission Date', default=fields.Date.today)
    note = fields.Text(string='Note')
    progress = fields.Integer(string='Progress Percentage')
    
    document_ids = fields.One2many('akademik.tesis.dokumen', 'thesis_id', string='Thesis Documents')
    seminar_schedule = fields.Datetime(string='Seminar Schedule')

    progress_category = fields.Selection([
        ('low', 'Low (0-49%)'),
        ('medium', 'Medium (50-99%)'),
        ('high', 'High (100%)')
    ], compute='_compute_progress_category', string='Progress Category')

    def action_request_approval(self):
        for record in self:
            record.stage = 'supervisor_appointment'

    def action_approve_supervisor(self):
        for record in self:
            record.student_id.sudo().dosen_pembimbing_id = record.supervisor_id
            record.stage = 'proposal_seminar'

    def action_reject_supervisor(self):
        for record in self:
            if not record.note:
                raise models.ValidationError(" fill in the note before rejecting.")
            record.stage = 'title_submission'

    def action_approve_proposal(self):
        for record in self:
            proposal = record.document_ids.filtered(lambda d: d.type == 'proposal' and d.status == 'verified')
            if not proposal:
                raise models.ValidationError("upload and verify the Proposal document before proceeding to Research stage.")
            
            if not record.seminar_schedule:
                raise models.ValidationError("set the Seminar Schedule before approving the proposal.")

            record.stage = 'research'

    def action_approve_research(self):
        for record in self:
            research_doc = record.document_ids.filtered(lambda d: d.type == 'research' and d.status == 'verified')
            if not research_doc:
                 raise models.ValidationError("upload and verify the Research document before proceeding to Final Defense.")
            
            record.stage = 'final_defense'

    def action_approve_defense(self):
        for record in self:
            if record.supervisor_id.user_id != self.env.user:
                raise models.ValidationError("Access Denied: Only the appointed Supervisor can approve the Final Defense.")

            if not record.defense_schedule:
                raise models.ValidationError("Please set the Final Defense Schedule.")
            
            if not record.examiner_score_ids:
                raise models.ValidationError("Please assign at least one Examiner.")

            unscored = record.examiner_score_ids.filtered(lambda s: s.score == 0)
            if unscored:
                raise models.ValidationError("All examiners must input a score (greater than 0) before approval.")

            record.sudo().stage = 'graduation'

    def action_cancel(self):
        for record in self:
            record.stage = 'title_submission'

    @api.depends('examiner_score_ids.score')
    def _compute_final_score(self):
        for record in self:
            if record.examiner_score_ids:
                total_score = sum(record.examiner_score_ids.mapped('score'))
                record.final_score = total_score / len(record.examiner_score_ids)
            else:
                record.final_score = 0

    defense_schedule = fields.Datetime(string='Final Defense Schedule')
    examiner_score_ids = fields.One2many('akademik.tesis.nilai', 'thesis_id', string='Examiner Scores')
    final_score = fields.Integer(string='Final Score', compute='_compute_final_score', store=True)

    @api.depends('progress')
    def _compute_progress_category(self):
        for record in self:
            if record.progress == 100:
                record.progress_category = 'high'
            elif record.progress >= 50:
                record.progress_category = 'medium'
            else:
                record.progress_category = 'low'

    stage = fields.Selection([
        ('title_submission', 'Title Submission'),
        ('supervisor_appointment', 'Supervisor Appointment'),
        ('proposal_seminar', 'Proposal Seminar'),
        ('research', 'Research'),
        ('final_defense', 'Final Defense'),
        ('graduation', 'Graduation')
    ], string='Stage', default='title_submission', group_expand='_expand_stage')

    @api.model
    def _expand_stage(self, states, domain, order):
        return [key for key, val in type(self).stage.selection]
