from odoo import models, fields, api

class Payslip(models.Model):
    _name = 'payroll.payslip'
    _description = 'Payslip'

    employee_id = fields.Many2one('payroll.employee', string='Employee', required=True)
    contract_id = fields.Many2one('payroll.contract', string='Contract', required=True)
    month = fields.Selection([(str(num), str(num)) for num in range(1, 13)], string='Month', required=True)
    year = fields.Integer(string='Year', required=True)
    working_days = fields.Integer(string='Working Days in Month', default=26, required=True)
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary', store=True)

    @api.depends('contract_id', 'working_days')
    def _compute_total_salary(self):
        for record in self:
            if record.contract_id and record.working_days:
                # default working in a month 22 days
                base_salary_per_day = record.contract_id.basic_salary / 22
                record.total_salary = (
                    base_salary_per_day * record.working_days +
                    record.contract_id.lunch_allowance +
                    record.contract_id.weekend_ot +
                    record.contract_id.holiday_ot +
                    record.contract_id.bonus -
                    (record.contract_id.employee_si +
                     record.contract_id.employee_hi +
                     record.contract_id.employee_ui)
                )
            else:
                record.total_salary = 0.0