{
    'name': 'Project Management',
    'version': '16.0.1.0.0',
    'category': 'Services/Project',
    'depends': ['task', 'hr', 'analytic'],
    'description': """
    Organize and plan your projects
    """,
    'assets': {
        'web.assets_backend': [
        ],
    },
    'data': [
        'security/project_groups.xml',
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/project_data.xml',
        'views/project_role_views.xml',
        'views/project_member_views.xml',
        'views/project_tag_views.xml',
        'views/project_stage_views.xml',
        'views/project_project_views.xml',
        'views/task_task_views.xml',
        'views/project_menus.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3'
}
