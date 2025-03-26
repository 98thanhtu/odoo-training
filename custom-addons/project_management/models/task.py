from odoo import models, fields, api

class Task(models.Model):
    _name = 'pr.task'
    _description = 'Task'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string="Task Name", required=True)
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    sprint_id = fields.Many2one('pr.sprint', string="Sprint")
    dev_id = fields.Many2one('pr.member', string="Developer")
    qc_id = fields.Many2one('pr.member', string="Quality Control")
    task_type_id = fields.Many2one('pr.task.type', string="Task Type")
    dev_deadline = fields.Date(string="Dev Deadline")
    qc_deadline = fields.Date(string="QC Deadline")
    status = fields.Selection([
        ('new', 'New'),
        ('dev', 'In Development'),
        ('qc', 'Quality Control'),
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
