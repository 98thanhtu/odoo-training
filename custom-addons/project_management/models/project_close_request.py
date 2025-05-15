from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class ProjectCloseRequest(models.Model):
    _name = 'pr.close.request'
    _description = 'Project Closing Request'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    project_id = fields.Many2one('pr.project', string="Project", required=True)
    pm_id = fields.Many2one('pr.member', string="Project Manager")
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
        if not vals.get('pm_id'):
            current_user = self.env.user
            current_pm = self.env['pr.member'].search([('user_id', '=', current_user.id)], limit=1)
            if current_pm:
                vals['pm_id'] = current_pm.id

        if current_user.has_group('project_management.group_project_admin') and not vals.get('status'):
            vals['status'] = 'submitted'

        record = super(ProjectCloseRequest, self).create(vals)
        record.code = f"RCJ{record.id:05d}"
        return record


    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            self.pm_id = self.project_id.pm_id

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        current_user = self.env.user
        current_pm = self.env['pr.member'].search([('user_id', '=', current_user.id)], limit=1)
        if current_pm:
            res['pm_id'] = current_pm.id
        return res

    @api.onchange('pm_id')
    def _onchange_pm_id(self):
        if self.pm_id:
            return {
                'domain': {
                    'project_id': [('pm_id', '=', self.pm_id.id)]
                }
            }

    @api.constrains('project_id')
    def _check_project_closed(self):
        for record in self:
            project = record.project_id

            sprints = self.env['pr.sprint'].search([('project_id', '=', project.id)])
            tasks = self.env['pr.task'].search([('project_id', '=', project.id)])

            if sprints:
                open_sprints = sprints.filtered(lambda s: s.status == 'open')
                if open_sprints:
                    raise ValidationError("Cannot create project close request because there are unclosed sprints.")

            if tasks:
                unfinished_tasks = tasks.filtered(lambda t: t.status != 'done')
                if unfinished_tasks:
                    raise ValidationError("Cannot create project close request because there are unfinished tasks.")


    def submit_request(self):
        for record in self:
            if record.status != 'draft':
                raise ValidationError("Only draft requests can be submitted.")
            record.status = 'submitted'

    def approve_request(self):
        for record in self:
            if record.status != 'submitted':
                raise ValidationError("Only submitted requests can be approved.")

            project = record.project_id
            project.end_date = record.end_date
            project.state = 'close'

            record.status = 'approved'

            if record.create_uid and record.create_uid.email:
                subject = _("Phiếu yêu cầu đóng dự án: %s đã được duyệt") % record.code
                body = _("""
Chào %s,

Phiếu yêu cầu đóng dự án của bạn đã được duyệt.

Trân trọng,
""") % record.create_uid.name

                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': f"<pre>{body}</pre>",
                    'email_to': record.create_uid.email,
                    'auto_delete': True,
                }).send()

    def cancel_request(self, reason=""):
        for record in self:
            if record.status not in ('draft', 'submitted'):
                raise ValidationError("Only draft or submitted requests can be cancelled.")

            record.status = 'cancelled'
            record.cancel_reason = reason

            if record.create_uid and record.create_uid.email:
                subject = _("Phiếu yêu cầu đóng dự án: %s đã bị huỷ") % record.code
                body = _("""
Chào %s,

Phiếu yêu cầu đóng dự án của bạn đã bị huỷ bởi %s với lý do: %s. Bạn vui lòng kiểm tra lại thông tin.

Trân trọng,
""") % (
    record.create_uid.name,
    self.env.user.name,
    reason or "Không có lý do"
)

                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': f"<pre>{body}</pre>",
                    'email_to': record.create_uid.email,
                    'auto_delete': True,
                }).send()
