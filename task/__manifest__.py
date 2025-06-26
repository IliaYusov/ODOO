{
    'name': 'Task Management',
    'version': '1.2.5',
    'category': '',
    'depends': ['base', 'mail', 'crnd_web_diagram_plus', 'hr', 'hr_replacement'],
    'external_dependencies': {'python': ['html2text']},
    'description': """
    """,
    'author': '',
    'support': '',
    'application': True,
    'installable': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'task/static/src/scss/task_form.scss',
            'task/static/src/components/**/*',
            'task/static/src/views/**/*'
        ]
    },
    'data': [
        'data/mail_template_data.xml',
        'data/task_data.xml',
        'data/ir_cron_data.xml',
        'security/task_security.xml',
        'security/ir.model.access.csv',
        'views/task_task_views.xml',
        'views/task_type_views.xml',
        'views/task_stage_views.xml',
        'views/task_stage_type_views.xml',
        'views/task_stage_route_views.xml',
        'views/res_config_settings.xml',
        'views/task_menus.xml',
        'report/task_task_report_analysis_views.xml',
        'wizard/task_close_wizard.xml'
    ],
    'demo': [
    ],
    'license': 'LGPL-3'
}
