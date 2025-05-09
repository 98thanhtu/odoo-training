from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class ProjectOpenRequest(models.Model):
    _name = 'pr.open.request'
    _description = 'Project Opening Request'

    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    project_name = fields.Char(string="Project Name", required=True)
    pm_id = fields.Many2one('pr.member', string="Project Manager", required=True)
    dev_ids = fields.Many2many('pr.member', 'pr_open_request_dev_rel', 'request_id', 'member_id', string="Developers")
    qc_ids = fields.Many2many('pr.member', 'pr_open_request_qc_rel', 'request_id', 'member_id', string="QC")
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    description = fields.Text(string="Description")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')
    cancel_reason = fields.Text(string="Cancel Reason")
    project_id = fields.Many2one('pr.project', string="Project", readonly=True)

    def approve_request(self):
        for record in self:
            if record.status != 'submitted':
                raise ValidationError("Only submitted requests can be approved.")

            project = self.env['pr.project'].create({
                'name': record.project_name,
                'pm_id': record.pm_id.id,
                'dev_ids': [(6, 0, record.dev_ids.ids)],
                'qc_ids': [(6, 0, record.qc_ids.ids)],
                'start_date': record.start_date,
                'description': record.description,
                'request_id': record.id
            })

            record.status = 'approved'
            record.project_id = project.id

            if record.create_uid and record.create_uid.email:
                template_subject = _("Phiếu yêu cầu tạo dự án: %s đã được duyệt") % record.code
                template_body = _("""
                Chào %s,

                Phiếu yêu cầu mở dự án của bạn đã được duyệt. Vui lòng liên hệ với các thành viên trong dự án để thông báo thông tin đến họ.

                Trân trọng,
                """) % record.create_uid.name

                mail_values = {
                    'subject': template_subject,
                    'body_html': f"<pre>{template_body}</pre>",
                    'email_to': record.create_uid.email,
                    'auto_delete': True,
                }
                self.env['mail.mail'].create(mail_values).send()

    def submit_request(self):
        for record in self:
            if record.status != 'draft':
                raise ValidationError("Only drafts are sent for approval")
            record.status = 'submitted'

    def cancel_request(self):
        for record in self:
            if record.status not in ('draft', 'submitted'):
                raise ValidationError("Only draft or submitted request can be canceled")
            record.status = 'cancelled'

    def action_approve_all_open_requests(self):
        requests = self.env['pr.open.request'].search([('status', '=', 'submitted')])
        for req in requests:
            req.approve_request()
        return True

    def action_refuse_all_open_requests(self):
        requests = self.search([('status', '=', 'submitted')])
        for req in requests:
            req.cancel_request()
        return True

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for pr in self:
            if pr.end_date and pr.end_date < pr.start_date:
                raise ValidationError('End Date must be greater than Start Date!')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        member = self.env['pr.member'].search([('user_id', '=', self.env.uid)], limit=1)
        if member and member.role == 'pm':
            res['pm_id'] = member.id
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        member = self.env['pr.member'].search([('user_id', '=', self.env.uid)], limit=1)
        is_pm_user = member and member.role == 'pm'
        res['context'] = res.get('context', {})
        res['context'].update({'is_pm_user': is_pm_user})
        return res

    @api.model
    def create(self, vals):
        record = super(ProjectOpenRequest, self).create(vals)
        record.code = f"ROP{record.id:05d}"
        return record
