{
    "name": "Contract Management",
    "version": "1.0.0",
    "category": "Contract Management",
    "license": "LGPL-3",
    "website": "",
    "author": "",
    "depends": ['base', 'hr', 'project_budget'],
    "data": [
        'data/contract_data.xml',
        'security/contract_security.xml',
        'security/ir.model.access.csv',
        'views/contract_views.xml',
        'views/contract_type_views.xml',
        'views/res_partner.xml',
        'views/contract_menu.xml'
    ],
    "assets": {
        "web.assets_backend": [
        ]
    },
    "demo": [
    ],
    "images": ["static/description/icon.png"],
    "application": True
}
