from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PrTaskSprintReport(models.TransientModel):
    _name = 'pr.task.report.sprint'
    _description = 'Task Report In Sprint'
    _auto = False
    _log_access = True

    project_id = fields.Many2one('pr.project', string='Project')
    sprint_id = fields.Many2one('pr.sprint', string='Sprint')
    member_id = fields.Many2one('res.users', string='Member')
    role = fields.Selection([('dev', 'Dev'), ('qc', 'QC')], string='Role')
    total_task = fields.Integer(string='Total Tasks')
    task_new = fields.Integer(string='New Tasks')
    task_dev = fields.Integer(string='Dev Tasks')
    task_qc = fields.Integer(string='QC Tasks')
    task_done = fields.Integer(string='Done Tasks')

    def show_all_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'pr.task',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.project_id.id)],
            'target': 'current',
        }
