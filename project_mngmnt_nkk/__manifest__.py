{
    'name': 'Project Management: NKK',
    'version': '16.0.1.0.0',
    'category': 'Services/Project',
    'depends': ['project_mngmnt', 'document_flow'],
    'description': """
    Customize 'Project Management' module for NKK
    """,
    'assets': {
        'web.assets_backend': [
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        # 'data/project_data.xml',
        'views/project_type_views.xml',
        'views/project_project_views.xml',
        # 'views/document_flow_document_views.xml',
        'views/project_menus.xml'
    ],
    'installable': True,
    'auto_install': ['project_mngmnt'],
    'license': 'LGPL-3'
}
