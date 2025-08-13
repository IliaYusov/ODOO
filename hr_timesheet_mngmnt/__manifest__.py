{
    'name': 'Task Timesheets',
    'version': '16.0.1.0.0',
    'category': 'Services/Timesheets',
    'summary': 'Track employee time on tasks',
    'description': """This module implements a timesheet system.""",
    'depends': ['hr', 'analytic', 'uom', 'task', 'project_mngmnt'],
    'data': [
        'security/hr_timesheet_groups.xml',
        'security/ir.model.access.csv',
        'data/hr_timesheet_data.xml',
        'views/hr_timesheet_views.xml',
        'views/project_account_method_employee_rate_views.xml',
        'views/project_role_views.xml',
        'views/project_project_views.xml',
        'views/task_task_views.xml',
        'views/project_member_views.xml',
        'views/res_config_settings_views.xml',
        'report/hr_timesheet_report_analysis_views.xml',
        'report/task_task_report_analysis_views.xml',
        'views/hr_timesheet_menus.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'assets': {
        'web.assets_backend': [
        ],
    },
    'license': 'LGPL-3'
}
