from odoo import models, fields, api
from datetime import datetime, timedelta

class Payslip(models.Model):
    _name = 'payroll.payslip'
    _description = 'Payslip'

    employee_id = fields.Many2one('payroll.employee', string='Employee', required=True)
    contract_id = fields.Many2one('payroll.contract', string='Contract', required=True, compute='_compute_contract', store=True)
    month = fields.Selection([(str(num), str(num)) for num in range(1, 13)], string='Month', required=True)
    year = fields.Integer(string='Year', compute='_compute_contract', store=True)
    working_days = fields.Integer(string='Working Days', compute='_compute_working_days', store=True)
    standard_working_days = fields.Integer(string='Standard Working Days', compute='_compute_standard_working_days', store=True)
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary', store=True)

    @api.depends('employee_id')
    def _compute_contract(self):
        today = fields.Date.today()
        for record in self:
            if record.employee_id:
                contracts = self.env['payroll.contract'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('start_date', '<=', today),
                    ('end_date', '>=', today)
                ], order='start_date ASC')

                if contracts:
                    record.contract_id = contracts[0]
                    record.year = record.contract_id.start_date.year
                else:
                    record.contract_id = False
                    record.year = False
            else:
                record.contract_id = False
                record.year = False

    @api.depends('employee_id', 'month', 'year')
    def _compute_working_days(self):
        for record in self:
            if record.employee_id and record.month and record.year:
                start_date = datetime(record.year, int(record.month), 1).date()
                end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

                attendances = self.env['payroll.attendance'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('check_in', '>=', start_date),
                    ('check_in', '<=', end_date)
                ])

                record.working_days = len(set(att.check_in.date() for att in attendances))
            else:
                record.working_days = 0

    @api.depends('month', 'year')
    def _compute_standard_working_days(self):
        for record in self:
            if record.month and record.year:
                start_date = datetime(record.year, int(record.month), 1).date()
                end_date = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

                work_days = sum(1 for day in range((end_date - start_date).days + 1)
                                if (start_date + timedelta(days=day)).weekday() < 5)
                record.standard_working_days = work_days
            else:
                record.standard_working_days = 0

    @api.depends('contract_id', 'working_days', 'standard_working_days')
    def _compute_total_salary(self):
        for record in self:
            if record.contract_id and record.working_days and record.standard_working_days:
                base_salary_per_day = record.contract_id.basic_salary / record.standard_working_days
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
