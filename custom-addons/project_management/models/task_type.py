from odoo import models, fields

class TaskType(models.Model):
    _name = 'pr.task.type'
    _description = 'Task Type'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    name = fields.Char(string="Task Type Name", required=True)
    active = fields.Boolean(string="Active", default=True)

    @api.model
    def create(self, vals):
        record = super(TaskType, self).create(vals)
        record.code = f"TT{record.id:05d}"
        return record
