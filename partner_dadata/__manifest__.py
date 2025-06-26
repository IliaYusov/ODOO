{
    'name': 'Partner: DaData Integration',
    'summary': 'Auto-complete partner companies information',
    'version': '1.0.0',
    'description': """
       Auto-complete partner information
    """,
    'category': 'Hidden/Tools',
    'depends': [
        'contacts_extended'
    ],
    'external_dependencies': {'python': ['dadata']},
    'assets': {
        'web.assets_backend': [
            'partner_dadata/static/src/views/**/*.js',
            'partner_dadata/static/src/views/**/*.xml'
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/partner_dadata_data.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/partner_load_info_views.xml'
    ],
    'license': 'LGPL-3'
}
