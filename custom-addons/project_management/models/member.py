from odoo import models, fields

class ProjectMember(models.Model):
    _name = 'pr.member'
    _description = 'Project Member'

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    date_of_birth = fields.Date(string='Date Of Birth')
    user_id = fields.Many2one('res.users', string='Related User', required=True)
    project_ids = fields.Many2many(
        'pr.project',
        'pr_project_member_rel',
        'member_id',
        'project_id',
        string="Projects"
    )
    role = fields.Selection([
        ('pm', 'Project Manager'),
        ('dev', 'Developer'),
        ('qc', 'QC')
    ], string="Role", required=True)
