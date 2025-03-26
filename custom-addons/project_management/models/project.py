from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Project(models.Model):
    _name = 'pr.project'
    _description = 'Project Management'

    name = fields.Char(string='Name', required=True, unique=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Close')
    ], default='closed', string='Status')
    pm_id = fields.Many2one('pr.member', string="Project Manager", required=True)
    dev_ids = fields.Many2many('pr.member', 'pr_project_dev_rel', 'request_id', 'member_id', string="Developers")
    qc_ids = fields.Many2many('pr.member', 'pr_project_qc_rel', 'request_id', 'member_id', string="QC")
    description = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        record = super(Project, self).create(vals)
        record.code = f"PRJ{record.id:05d}"
        return record

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for pr in self:
            if pr.end_date and pr.end_date < pr.start_date:
                raise ValidationError('End Date must be greater than Start Date!')
