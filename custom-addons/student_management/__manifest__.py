# -*- coding: utf-8 -*-
{
    'name': "Student Management",

    'summary': "Test Summary",

    'description': """
Long description of module's purpose
    """,

    'author': "Thanh Tu",
    'website': "https://www.fb.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/student_views.xml',
        'security/student_security.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
