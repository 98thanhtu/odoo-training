from odoo import models, fields, api

class Sprint(models.Model):
    _name = 'pr.sprint'
    _description = 'Sprint'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string="Sprint Name", required=True)
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string="Status", default='draft')

    @api.model
    def create(self, vals):
        record = super(Sprint, self).create(vals)
        record.code = f"SPR{record.id:05d}"
        return record

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for pr in self:
            if pr.end_date and pr.end_date < pr.start_date:
                raise ValidationError('End Date must be greater than Start Date!')
