from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Project(models.Model):
    _name = 'pr.project'
    _description = 'Project Management'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Close')
    ], default='closed', string='Status')
    pm_id = fields.Many2one('pr.member', string="Project Manager", required=True, domain=[('role', '=', 'pm')])
    dev_ids = fields.Many2many('pr.member', 'pr_project_dev_rel', 'request_id', 'member_id', string="Developers", domain=[('role', '=', 'dev')])
    qc_ids = fields.Many2many('pr.member', 'pr_project_qc_rel', 'request_id', 'member_id', string="QC", domain=[('role', '=', 'qc')])
    description = fields.Text(string='Description')
    task_ids = fields.One2many('pr.task', 'project_id', string="Tasks")
    task_count = fields.Integer(string="Task Count", compute="_compute_task_count")
    request_id = fields.Many2one('pr.open.request', string='Open Request')

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

    def action_close(self):
        for record in self:
            record.state = 'closed'

    def open_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Tasks',
            'res_model': 'pr.task',
            'view_mode': 'kanban,tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'default_sprint_id': self.env['pr.sprint'].search([
                    ('project_id', '=', self.id),
                    ('status', '=', 'open')
                ], order='create_date desc', limit=1).id or False,
            },
            'target': 'current',
        }

    @api.depends('task_ids')
    def _compute_task_count(self):
        for project in self:
            project.task_count = len(project.task_ids)

    def edit_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Project',
            'res_model': 'pr.project',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.constrains('name')
    def _check_unique_name(self):
        for project in self:
            existing_project = self.env['pr.project'].search([
                ('name', 'ilike', project.name),
                ('id', '!=', project.id)
            ], limit=1)
            if existing_project:
                raise ValidationError("Project Name must be unique.")

    def weekly_report(self):
        print(self)
        print('=================== Test Schedule ===================')
