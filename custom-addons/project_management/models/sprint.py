from odoo import models, fields

class Sprint(models.Model):
    _name = 'pr.sprint'
    _description = 'Sprint'

    code = fields.Char(string="Sprint Code", required=True, copy=False, readonly=True, default=lambda self: 'New')
    name = fields.Char(string="Sprint Name", required=True)
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string="Status", default='draft')
