from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Attendance(models.Model):
    _name = 'payroll.attendance'
    _description = 'Attendance'

    employee_id = fields.Many2one('payroll.employee', string='Employee', required=True)
    check_in = fields.Datetime(string='Check In', required=True)
    check_out = fields.Datetime(string='Check Out', required=True)
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.worked_hours = delta.total_seconds() / 3600
            else:
                record.worked_hours = 0.0

    # @api.model
    # def create(self, vals):
    #     attendance = super(PayrollAttendance, self).create(vals)

    #     payslip = self.env['payroll.payslip'].search([
    #         ('employee_id', '=', attendance.employee_id.id),
    #         ('month', '=', str(attendance.check_in.month)),
    #         ('year', '=', attendance.check_in.year)
    #     ], limit=1)

    #     if payslip:
    #         payslip._compute_total_hours()
    #         payslip._compute_total_salary()

    #     return attendance

    @api.constrains('check_in', 'check_out')
    def _check_check_in_out(self):
        for record in self:
            if record.check_in and record.check_out and record.check_in >= record.check_out:
                raise ValidationError("Check In must be before Check Out.")
