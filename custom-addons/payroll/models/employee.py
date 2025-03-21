from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Employee(models.Model):
    _name = 'payroll.employee'
    _description = 'Employee'

    name = fields.Char(string='Employee Name', required=True)
    avatar = fields.Binary(string='Avatar', attachment=True)
    address = fields.Char(string='Address')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    date_of_birth = fields.Datetime(string='Date Of Birth')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    contract_ids = fields.One2many('payroll.contract', 'employee_id', string='Contracts')
    user_id = fields.Many2one('res.users', string='Related User', required=True)

    @api.constrains('contract_ids')
    def _check_contracts(self):
        for employee in self:
            if not employee.contract_ids:
                raise ValidationError("An employee must have at least one contract.")
    def action_open_contract_form(self):
        return {
            'name': 'New Contract',
            'type': 'ir.actions.act_window',
            'res_model': 'payroll.contract',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_employee_id': self.id}
        }
