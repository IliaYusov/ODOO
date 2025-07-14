{
    'name': 'Helpdesk: Task',
    'version': '16.0.1.0.0',
    'category': 'Services/Helpdesk',
    'depends': ['helpdesk_mngmnt', 'task'],
    'description': """
    Bridge to convert tickets to tasks
    """,
    'installable': True,
    'data': [
        'views/task_task_views.xml',
        'views/helpdesk_ticket_views.xml'
    ],
    'license': 'LGPL-3'
}
