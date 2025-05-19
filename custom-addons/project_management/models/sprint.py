from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    def write(self, vals):
        if 'status' in vals and vals['status'] == 'open':
            for sprint in self:
                existing_open = self.search_count([
                    ('project_id', '=', sprint.project_id.id),
                    ('status', '=', 'open'),
                    ('id', '!=', sprint.id)
                ])
                if existing_open:
                    raise ValidationError("Only one sprint can be open per project at a time.")
        return super(Sprint, self).write(vals)
