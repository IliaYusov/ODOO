{
    'name': 'Project Management: Account Budget',
    'version': '16.0.1.0.0',
    'summary': 'Project account budget',
    'category': 'Services/Project',
    'depends': ['account_budget_mngmnt', 'project_mngmnt'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_project_views.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3'
}
