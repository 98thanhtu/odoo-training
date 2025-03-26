# -*- coding: utf-8 -*-
{
    'name': "Project Management",

    'summary': "Project Management",

    'description': """
Long description of module's purpose
    """,

    'author': "BAP",
    'website': "https://www.google.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/pr_member_views.xml',
        'views/pr_open_request_views.xml',
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
}

