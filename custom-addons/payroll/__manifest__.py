# -*- coding: utf-8 -*-
{
    'name': "Payroll",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
      'security/payroll_security.xml',
      'security/ir.model.access.csv',
      'views/hr_employee_views.xml',
      'views/hr_contract_views.xml',
      'views/hr_payslip_views.xml',
      'views/hr_attendance_views.xml',
    ],
    'installable': True,
    'application': True,
}

