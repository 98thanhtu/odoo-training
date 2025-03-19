from odoo import models, fields, api

class Contract(models.Model):
    _name = 'hr.contract'
    _description = 'Contract'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    basic_salary = fields.Float(string='Basic Salary')
    lunch_allowance = fields.Float(string='Lunch Allowance')
    weekend_ot = fields.Float(string='Weekend OT')
    holiday_ot = fields.Float(string='Holiday OT')
    bonus = fields.Float(string='Bonus')

    # Social Insurance Contributions
    company_si = fields.Float(string='Company Social Insurance (17%)', compute='_compute_insurances')
    employee_si = fields.Float(string='Employee Social Insurance (8%)', compute='_compute_insurances')

    # Health Insurance Contributions
    company_hi = fields.Float(string='Company Health Insurance (3%)', compute='_compute_insurances')
    employee_hi = fields.Float(string='Employee Health Insurance (1.5%)', compute='_compute_insurances')

    # Unemployment Insurance Contributions
    company_ui = fields.Float(string='Company Unemployment Insurance (0.5%)', compute='_compute_insurances')
    employee_ui = fields.Float(string='Employee Unemployment Insurance (1%)', compute='_compute_insurances')

    @api.depends('basic_salary')
    def _compute_insurances(self):
        for record in self:
            record.company_si = record.basic_salary * 0.17
            record.employee_si = record.basic_salary * 0.08
            record.company_hi = record.basic_salary * 0.03
            record.employee_hi = record.basic_salary * 0.015
            record.company_ui = record.basic_salary * 0.005
            record.employee_ui = record.basic_salary * 0.01
