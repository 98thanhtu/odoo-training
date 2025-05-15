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
        'data/pr_task_actions.xml',
        'views/pr_member_views.xml',
        'views/pr_open_request_views.xml',
        'views/pr_close_request_views.xml',
        'views/pr_project_views.xml',
        'views/pr_task_views.xml',
        'views/pr_task_type_views.xml',
        'views/pr_sprint_views.xml',
        'views/pr_menu_views.xml',
        'views/pr_report_views.xml',
        'security/project_groups.xml',
        'security/pr_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_job_weekly_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'project_management/static/src/js/month_year_widget.js',
            # 'project_management/static/src/xml/month_year_widget.xml',
            # 'web/static/lib/bootstrap-datepicker/js/bootstrap-datepicker.js',
            # 'web/static/lib/bootstrap-datepicker/css/bootstrap-datepicker.css',
            # 'project_management/static/src/css/clickable_integer.scss'
        ],
    },
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
}

