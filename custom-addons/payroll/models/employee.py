from odoo import models, fields

class Employee(models.Model):
    _name = 'hr.employee'
    _description = 'Employee'

    name = fields.Char(string='Employee Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    contract_ids = fields.One2many('hr.contract', 'employee_id', string='Contracts')
    user_id = fields.Many2one('res.users', string='Related User', required=True)

