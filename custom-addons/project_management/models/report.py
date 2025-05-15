from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class ReportDeadlineUrgent(models.Model):
    _name = 'report.deadline.urgent'
    _description = 'Report Deadline Urgent'
    _auto = False
    _order = 'deadline desc'

    code = fields.Char(string="Task Code", readonly=True)
    name = fields.Char(string="Task Name", readonly=True)
    project_id = fields.Many2one('pr.project', string="Project", readonly=True)
    member_id = fields.Many2one('pr.member', string="Assigned Member", readonly=True)
    deadline = fields.Date(string="Deadline", readonly=True)
    status = fields.Selection([
        ('new', 'New'),
        ('dev', 'In Development'),
        ('qc', 'QC'),
        ('done', 'Done')
    ], string="Status", readonly=True)

    def init(self):
        """Initialize the SQL view for the report."""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW report_deadline_urgent AS (
                SELECT
                    t.id,
                    t.code,
                    t.name,
                    t.project_id,
                    t.dev_id AS member_id,
                    t.dev_deadline AS deadline,
                    t.status
                FROM pr_task t
                WHERE t.dev_deadline IS NOT NULL
                    AND t.dev_deadline <= %s
                    AND t.dev_deadline >= CURRENT_DATE
                UNION
                SELECT
                    t.id,
                    t.code,
                    t.name,
                    t.project_id,
                    t.qc_id AS member_id,
                    t.qc_deadline AS deadline,
                    t.status
                FROM pr_task t
                WHERE t.qc_deadline IS NOT NULL
                    AND t.qc_deadline <= %s
                    AND t.qc_deadline >= CURRENT_DATE
            )
        """, [fields.Date.today() + timedelta(days=2)] * 2)

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """Apply access restrictions based on user groups."""
        user = self.env.user
        if not user.has_group('project_management.group_project_admin'):
            if user.has_group('project_management.group_project_pm'):
                pm_projects = self.env['pr.project'].search([('pm_id.user_id', '=', user.id)]).ids
                domain = [('project_id', 'in', pm_projects)] + domain
            else:
                domain = [('project_id', '=', False)] + domain  # No access for non-PM/non-Admin
        return super()._read_group_raw(domain, fields, groupby, offset, limit, orderby, lazy)

class ReportTaskSprintWizard(models.TransientModel):
    _name = 'report.task.sprint.wizard'
    _description = 'Task in Sprint Report Wizard'

    date_from = fields.Date(string="From Date", required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(string="To Date", required=True, default=lambda self: (fields.Date.today().replace(day=1) + relativedelta(months=1) - relativedelta(days=1)))
    project_ids = fields.Many2many('pr.project', string="Projects")

    def action_generate_report(self):
        """Generate the Task in Sprint report."""
        user = self.env.user
        project_domain = []
        if self.project_ids:
            project_domain = [('id', 'in', self.project_ids.ids)]
        else:
            if not user.has_group('project_management.group_project_admin'):
                if user.has_group('project_management.group_project_pm'):
                    project_domain = [('pm_id.user_id', '=', user.id)]
                else:
                    project_domain = [('id', '=', False)]  # No access

        projects = self.env['pr.project'].search(project_domain)
        report_lines = []

        for project in projects:
            sprints = self.env['pr.sprint'].search([
                ('project_id', '=', project.id),
                ('start_date', '>=', self.date_from),
                ('end_date', '<=', self.date_to)
            ])

            for sprint in sprints:
                # Process DEV members
                for member in project.dev_ids:
                    tasks = self.env['pr.task'].search([
                        ('project_id', '=', project.id),
                        ('sprint_id', '=', sprint.id),
                        ('dev_id', '=', member.id)
                    ])
                    if tasks:
                        report_lines.append({
                            'member_id': member.id,
                            'project_id': project.id,
                            'sprint_id': sprint.id,
                            'role': 'DEV',
                            'total_task': len(tasks),
                            'new_task': len(tasks.filtered(lambda t: t.status == 'new')),
                            'dev_task': len(tasks.filtered(lambda t: t.status == 'dev')),
                            'qc_task': len(tasks.filtered(lambda t: t.status == 'qc')),
                            'done_task': len(tasks.filtered(lambda t: t.status == 'done')),
                        })

                # Process QC members
                for member in project.qc_ids:
                    tasks = self.env['pr.task'].search([
                        ('project_id', '=', project.id),
                        ('sprint_id', '=', sprint.id),
                        ('qc_id', '=', member.id)
                    ])
                    if tasks:
                        report_lines.append({
                            'member_id': member.id,
                            'project_id': project.id,
                            'sprint_id': sprint.id,
                            'role': 'QC',
                            'total_task': len(tasks),
                            'new_task': len(tasks.filtered(lambda t: t.status == 'new')),
                            'dev_task': len(tasks.filtered(lambda t: t.status == 'dev')),
                            'qc_task': len(tasks.filtered(lambda t: t.status == 'qc')),
                            'done_task': len(tasks.filtered(lambda t: t.status == 'done')),
                        })

        # Create report records
        self.env['report.task.sprint'].search([]).unlink()  # Clear existing records
        for line in report_lines:
            self.env['report.task.sprint'].create(line)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Task in Sprint Report',
            'res_model': 'report.task.sprint',
            'view_mode': 'tree',
            'target': 'current',
        }

class ReportTaskSprint(models.Model):
    _name = 'report.task.sprint'
    _description = 'Task in Sprint Report'

    member_id = fields.Many2one('pr.member', string="Member", required=True)
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    sprint_id = fields.Many2one('pr.sprint', string="Sprint", required=True)
    role = fields.Char(string="Role", required=True)
    total_task = fields.Integer(string="Total Tasks")
    new_task = fields.Integer(string="New Tasks")
    dev_task = fields.Integer(string="Dev Tasks")
    qc_task = fields.Integer(string="QC Tasks")
    done_task = fields.Integer(string="Done Tasks")

    def show_all_tasks(self):
        """Show all tasks for the project and sprint."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'pr.task',
            'view_mode': 'tree,form',
            'domain': [
                ('project_id', '=', self.project_id.id),
                ('sprint_id', '=', self.sprint_id.id),
                '|', ('dev_id', '=', self.member_id.id), ('qc_id', '=', self.member_id.id)
            ],
            'context': {'default_project_id': self.project_id.id},
            'target': 'new',
        }

    def show_new_tasks(self):
        """Show new tasks."""
        self.ensure_one()
        return self._show_tasks_by_status('new')

    def show_dev_tasks(self):
        """Show dev tasks."""
        self.ensure_one()
        return self._show_tasks_by_status('dev')

    def show_qc_tasks(self):
        """Show qc tasks."""
        self.ensure_one()
        return self._show_tasks_by_status('qc')

    def show_done_tasks(self):
        """Show done tasks."""
        self.ensure_one()
        return self._show_tasks_by_status('done')

    def _show_tasks_by_status(self, status):
        """Helper method to show tasks by status."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'{status.title()} Tasks',
            'res_model': 'pr.task',
            'view_mode': 'tree,form',
            'domain': [
                ('project_id', '=', self.project_id.id),
                ('sprint_id', '=', self.sprint_id.id),
                ('status', '=', status),
                '|', ('dev_id', '=', self.member_id.id), ('qc_id', '=', self.member_id.id)
            ],
            'context': {'default_project_id': self.project_id.id},
            'target': 'new',
        }
