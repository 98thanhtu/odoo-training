from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PayrollAttendance(models.Model):
    _name = 'payroll.attendance'
    _description = 'Payroll Attendance'

    employee_id = fields.Many2one('payroll.employee', string='Employee', required=True)
    check_in = fields.Datetime(string='Check In', required=True)
    check_out = fields.Datetime(string='Check Out', required=True)
    hours_worked = fields.Float(string='Hours Worked', compute='_compute_hours_worked', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string='Status', default='draft')

    @api.depends('check_in', 'check_out')
    def _compute_hours_worked(self):
        for record in self:
            if record.check_in and record.check_out:
                duration = record.check_out - record.check_in
                record.hours_worked = duration.total_seconds() / 3600  # Chuyển thành giờ

    @api.model
    def create(self, vals):
        attendance = super(PayrollAttendance, self).create(vals)
        attendance.state = 'confirmed'
        return attendance

    def unlink(self):
        for record in self:
            if record.state == 'confirmed' and not self.env.user.has_group('payroll.group_hr_manager'):
                raise ValidationError("You are not allowed to delete confirmed attendance records.")
        return super(PayrollAttendance, self).unlink()
