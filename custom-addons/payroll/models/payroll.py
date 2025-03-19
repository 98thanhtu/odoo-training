from odoo import models, fields, api

class Payroll(models.Model):
    _name = 'hr.payroll'
    _description = 'Payroll'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True)
    month = fields.Selection([(str(num), str(num)) for num in range(1, 13)], string='Month', required=True)
    year = fields.Integer(string='Year', required=True)
    working_days = fields.Integer(string='Working Days in Month')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary')

    @api.depends('contract_id', 'working_days')
    def _compute_total_salary(self):
        for record in self:
            if record.contract_id:
                base_salary_per_day = record.contract_id.basic_salary / (record.working_days if record.working_days else 26)
                record.total_salary = (base_salary_per_day * record.working_days +
                                       record.contract_id.lunch_allowance +
                                       record.contract_id.weekend_ot +
                                       record.contract_id.holiday_ot +
                                       record.contract_id.bonus -
                                       (record.contract_id.employee_si +
                                        record.contract_id.employee_hi +
                                        record.contract_id.employee_ui))
