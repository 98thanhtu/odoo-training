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

    @api.constrains('start_date', 'end_date', 'project_id')
    def _check_sprint_constraints(self):
        for sprint in self:
            if sprint.end_date and sprint.end_date < sprint.start_date:
                raise ValidationError('End Date must be greater than Start Date!')

            overlapping_sprints = self.env['pr.sprint'].search([
                ('project_id', '=', sprint.project_id.id),
                ('id', '!=', sprint.id),
                '|',
                '&', ('start_date', '<=', sprint.start_date), ('end_date', '>=', sprint.start_date),
                '&', ('start_date', '<=', sprint.end_date), ('end_date', '>=', sprint.end_date)
            ])
            if overlapping_sprints:
                raise ValidationError('A project cannot have overlapping sprints!')

            open_sprints = self.env['pr.sprint'].search_count([
                ('project_id', '=', sprint.project_id.id),
                ('status', '=', 'open'),
                ('id', '!=', sprint.id)
            ])
            if sprint.status == 'open' and open_sprints > 0:
                raise ValidationError('A project can only have one open sprint at a time!')

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
