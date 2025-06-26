{
    'name': 'Authentication OpenID Connect',
    'summary': 'Allow users to login through OpenID Connect Provider',
    'version': '16.0.1.0.0',
    'external_dependencies': {'python': ['python-jose']},
    'depends': ['auth_oauth'],
    'data': [
        'views/auth_oauth_provider_views.xml'
    ],
    'license': 'LGPL-3'
}
