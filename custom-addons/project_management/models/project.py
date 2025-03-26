from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Project(models.Model):
    _name = 'pr.project'
    _description = 'Project Management'

    name = fields.Char(string='Name', required=True, unique=True)
    code = fields.Char(string='Code', readonly=True, copy=False)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Close')
    ], default='open', string='Status')
    pm_id = fields.Many2one('res.users', string='PM')
    dev_ids = fields.Many2many(
        'pr.member',
        'pr_project_dev_rel',
        'request_id',
        'member_id',
        string="Developers"
    )

    qc_ids = fields.Many2many(
        'pr.member',
        'pr_project_qc_rel',
        'request_id',
        'member_id',
        string="Quality Control"
    )
    description = fields.Text(string='Mô tả')

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('pr.project') or 'PRJ00001'
        return super(Project, self).create(vals)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for pr in self:
            if pr.end_date and pr.end_date < pr.start_date:
                raise ValidationError('End Date must be greater than Start Date!')
