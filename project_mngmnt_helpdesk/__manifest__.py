{
    'name': 'Project Management: Helpdesk',
    'version': '16.0.1.0.0',
    'category': 'Services',
    'depends': ['project_mngmnt', 'helpdesk_mngmnt', 'helpdesk_mngmnt_task'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_action_data.xml',
        'wizard/helpdesk_ticket_convert_to_task_views.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
