from odoo import models, fields, api
from datetime import timedelta, date

class PrDeadlineUrgentWizard(models.TransientModel):
    _name = 'pr.task.report.urgent'
    _description = 'Urgent Deadline Task Report'

    project_ids = fields.Many2many('pr.project', string='Projects')

    def action_show_report(self):
        domain = [('deadline', '<=', fields.Date.to_string(date.today() + timedelta(days=2)))]
        if self.project_ids:
            domain += [('project_id', 'in', self.project_ids.ids)]

        tasks = self.env['pr.task'].search(domain)
        self.env['pr.report.deadline.urgent'].search([]).unlink()

        for task in tasks:
            self.env['pr.report.deadline.urgent'].create({
                'task_id': task.id,
                'name': task.name,
                'project_id': task.project_id.id,
                'assign_member_id': task.assign_member_id.id,
                'deadline': task.deadline,
                'state': task.state,
            })

        return {
            'name': 'Deadline Urgent Tasks',
            'type': 'ir.actions.act_window',
            'res_model': 'pr.report.deadline.urgent',
            'view_mode': 'tree',
            'target': 'current',
        }
