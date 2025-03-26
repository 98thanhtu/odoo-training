from odoo import models, fields

class ProjectCloseRequest(models.Model):
    _name = 'dpr.close.request'
    _description = 'Project Closing Request'

    code = fields.Char(string="Request Code", required=True, copy=False, readonly=True, default=lambda self: 'New')
    project_id = fields.Many2one('dpr.project', string="Project", required=True)
    pm_id = fields.Many2one('dpr.member', string="Project Manager", required=True)
    end_date = fields.Date(string="End Date", required=True)
    close_reason = fields.Text(string="Close Reason")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')
    cancel_reason = fields.Text(string="Cancel Reason")
