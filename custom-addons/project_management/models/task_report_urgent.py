from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PrTaskReportUrgent(models.TransientModel):
    _name = 'pr.task.report.urgent'
    _description = 'Urgent Deadline Task Report'
    _log_access = True

    def _get_tasks(self):
        domain = [
            '|',
            ('dev_deadline', '<=', fields.Date.today() + timedelta(days=2)),
            ('qc_deadline', '<=', fields.Date.today() + timedelta(days=2)),
            ('status', '!=', 'done'),
        ]
        if self.env.user.has_group('project_management.group_project_pm'):
            domain += [('project_id.pm_id', '=', self.env.user.id)]
        elif self.env.user.has_group('project_management.group_project_member'):
            domain += [
                '|', '|',
                ('project_id.dev_ids', 'in', self.env.user.id),
                ('project_id.qc_ids', 'in', self.env.user.id),
                ('project_id.pm_id', '=', self.env.user.id),
            ]
        return self.env['pr.task'].search(domain, order="dev_deadline desc, qc_deadline desc")

    def open_report(self):
        tasks = self._get_tasks()
        action = self.env.ref('project_management.action_task_report_deadline_urgent').read()[0]
        action['domain'] = [('id', 'in', tasks.ids)]
        return action
