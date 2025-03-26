from odoo import models, fields

class TaskType(models.Model):
    _name = 'pr.task.type'
    _description = 'Task Type'

    code = fields.Char(string="Task Type Code", required=True, copy=False, readonly=True, default=lambda self: 'New')
    name = fields.Char(string="Task Type Name", required=True)
    active = fields.Boolean(string="Active", default=True)
