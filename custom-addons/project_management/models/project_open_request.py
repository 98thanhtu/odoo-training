from odoo import models, fields, api

class ProjectOpenRequest(models.Model):
    _name = 'pr.open.request'
    _description = 'Project Opening Request'

    code = fields.Char(string="Request Code", required=True, copy=False, readonly=True, default=lambda self: 'New')
    project_name = fields.Char(string="Project Name", required=True)
    pm_id = fields.Many2one('pr.member', string="Project Manager", required=True)
    dev_ids = fields.Many2many('pr.member', 'pr_open_request_dev_rel', 'request_id', 'member_id', string="Developers")
    qc_ids = fields.Many2many('pr.member', 'pr_open_request_qc_rel', 'request_id', 'member_id', string="Quality Control")
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
    project_id = fields.Many2one('pr.project', string="Linked Project", readonly=True)

    def approve_request(self):
        for record in self:
            if record.status != 'submitted':
                raise ValueError("Only submitted requests can be approved.")

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

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for pr in self:
            if pr.end_date and pr.end_date < pr.start_date:
                raise ValidationError('End Date must be greater than Start Date!')