from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Task(models.Model):
    _name = 'pr.task'
    _description = 'Task'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string="Task Name", required=True)
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    sprint_id = fields.Many2one('pr.sprint', string="Sprint", required=True)
    dev_id = fields.Many2one(
        'pr.member',
        string="Developer",
        domain="[('id', 'in', project_id.dev_ids)]"
    )
    qc_id = fields.Many2one(
        'pr.member',
        string="QC",
        domain="[('id', 'in', project_id.qc_ids)]"
    )
    task_type_id = fields.Many2one('pr.task.type', string="Task Type")
    dev_deadline = fields.Date(string="Dev Deadline")
    qc_deadline = fields.Date(string="QC Deadline")
    status = fields.Selection([
        ('new', 'New'),
        ('dev', 'In Development'),
        ('qc', 'QC'),
        ('done', 'Done')
    ], string="Status", default='new')
    description = fields.Text(string="Description")
    progress_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('blocked', 'Blocked'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string="Progress Status", default='not_started')

    @api.model
    def create(self, vals):
        record = super(Task, self).create(vals)
        record.code = f"T{record.id:05d}"
        return record

    def action_update_newest_sprint(self):
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            raise ValidationError("No project specified in the context.")

        # Find the newest open sprint
        newest_sprint = self.env['pr.sprint'].search([
            ('project_id', '=', project_id),
            ('status', '=', 'open')
        ], order='create_date desc', limit=1)

        if not newest_sprint:
            raise ValidationError("No open sprint found for this project.")

        active_ids = self.env.context.get('active_ids', [])
        tasks = self.env['pr.task'].browse(active_ids).filtered(
            lambda t: t.project_id.id == project_id and
                      t.sprint_id.status == 'closed' and
                      t.status != 'done'
        )

        if not tasks:
            tasks = self.env['pr.task'].search([
                ('project_id', '=', project_id),
                ('sprint_id.status', '=', 'closed'),
                ('status', '!=', 'done')
            ])

        if not tasks:
            raise ValidationError("No tasks to update to the newest sprint.")

        # Update tasks to the newest sprint
        tasks.write({'sprint_id': newest_sprint.id})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Updated {len(tasks)} tasks to sprint {newest_sprint.name}.',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.constrains('dev_id', 'dev_deadline', 'qc_id', 'qc_deadline')
    def _check_required_deadlines(self):
        for task in self:
            if task.dev_id and not task.dev_deadline:
                raise ValidationError("Dev Deadline is required when Developer is assigned.")
            if task.qc_id and not task.qc_deadline:
                raise ValidationError("QC Deadline is required when QC is assigned.")
