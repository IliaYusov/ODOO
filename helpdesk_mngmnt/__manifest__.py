{
    'name': 'Helpdesk',
    'version': '16.0.1.0.0',
    'category': 'Services/Helpdesk',
    'depends': ['base', 'portal'],
    'description': """
    Track, prioritize, and solve customer tickets
    """,
    'application': True,
    'installable': True,
    'auto_install': False,
    'data': [
        'security/helpdesk_groups.xml',
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/helpdesk_data.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_ticket_type_views.xml',
        'views/helpdesk_ticket_stage_views.xml',
        'views/helpdesk_portal_templates.xml',
        'views/helpdesk_menus.xml'
    ],
    'license': 'LGPL-3'
}
