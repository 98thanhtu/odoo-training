from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PayrollContract(models.Model):
    _name = 'payroll.contract'
    _description = 'Payroll Contract'

    employee_id = fields.Many2one('payroll.employee', string='Employee', required=True)
    contract_type = fields.Selection([
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ], string='Contract Type', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    job_position = fields.Char(string='Job Position')

    basic_salary = fields.Float(string='Basic Salary', required=True)
    lunch_allowance = fields.Float(string='Lunch Allowance', required=True)
    normal_ot = fields.Float(string='Normal OT')
    weekend_ot = fields.Float(string='Weekend OT')
    holiday_ot = fields.Float(string='Holiday OT')
    bonus = fields.Float(string='Bonus', required=True)

    # Social Insurance Contributions
    company_si = fields.Float(string='Company Social Insurance (17%)', compute='_compute_insurances', store=True)
    employee_si = fields.Float(string='Employee Social Insurance (8%)', compute='_compute_insurances', store=True)

    # Health Insurance Contributions
    company_hi = fields.Float(string='Company Health Insurance (3%)', compute='_compute_insurances', store=True)
    employee_hi = fields.Float(string='Employee Health Insurance (1.5%)', compute='_compute_insurances', store=True)

    # Unemployment Insurance Contributions
    company_ui = fields.Float(string='Company Unemployment Insurance (0.5%)', compute='_compute_insurances', store=True)
    employee_ui = fields.Float(string='Employee Unemployment Insurance (1%)', compute='_compute_insurances', store=True)

    @api.depends('basic_salary')
    def _compute_insurances(self):
        """ Calculate insurance benefits based on base salary """
        for record in self:
            record.company_si = record.basic_salary * 0.17
            record.employee_si = record.basic_salary * 0.08
            record.company_hi = record.basic_salary * 0.03
            record.employee_hi = record.basic_salary * 0.015
            record.company_ui = record.basic_salary * 0.005
            record.employee_ui = record.basic_salary * 0.01

    # @api.depends('basic_salary')
    # def _compute_overtimes(self):
    #     """ Calculate overtimes based on base salary """
    #     for record in self:
    #         record.normal_ot = record.basic_salary * 0.17

    @api.constrains('start_date', 'end_date')
    def _check_contract_dates(self):
        """ End Date must be greater than Start Date """
        for record in self:
            if record.end_date and record.start_date and record.end_date <= record.start_date:
                raise ValidationError("End Date must be greater than Start Date.")
