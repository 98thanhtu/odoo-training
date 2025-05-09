from odoo import models, fields, api

class ProjectCloseRequest(models.Model):
    _name = 'pr.close.request'
    _description = 'Project Closing Request'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    pm_id = fields.Many2one('pr.member', string="Project Manager", required=True)
    end_date = fields.Date(string="End Date", required=True)
    close_reason = fields.Text(string="Close Reason")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')
    cancel_reason = fields.Text(string="Cancel Reason")

    @api.model
    def create(self, vals):
        record = super(ProjectCloseRequest, self).create(vals)
        record.code = f"RCJ{record.id:05d}"
        return record

    @api.constrains('project_id')
    def _check_project_closed(self):
        for record in self:
            project = record.project_id
            sprints = project.sprint_ids
            tasks = project.task_ids

            open_sprints = sprints.filtered(lambda s: s.state != 'close')
            if open_sprints:
                raise ValidationError("Cannot create project close request because there are unclosed sprints.")

            unfinished_tasks = tasks.filtered(lambda t: t.state != 'done')
            if unfinished_tasks:
                raise ValidationError("Cannot create project close request because there are unfinished tasks.")

    def action_approve_all_close_requests(self):
        print(self)

    def action_refuse_all_close_requests(self):
        print(self)
