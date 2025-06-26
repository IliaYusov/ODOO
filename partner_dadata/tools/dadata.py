from dadata import Dadata


def _get_token(env):
    return env['ir.config_parameter'].sudo().get_param('partner_dadata.token', '')


def _get_secret(env):
    return env['ir.config_parameter'].sudo().get_param('partner_dadata.secret', '')


def get_partner_info_by_vat(env, vat):
    token = _get_token(env)
    secret = _get_secret(env)

    with Dadata(token, secret) as dadata:
        results = dadata.find_by_id(name='party', query=vat, count=1)
        if not any(results):
            return False
        org_info = results[0].get('data')
        return {
            'name': org_info.get('name').get('short_with_opf'),
            'full_name': org_info.get('name').get('full_with_opf'),
            'street': org_info.get('address').get('value'),
            'city': org_info.get('address').get('data').get('city'),
            'zip': org_info.get('address').get('data').get('postal_code'),
            'country_id': env['res.country'].search([
                ('code', '=', org_info.get('address').get('data').get('country_iso_code'))
            ], limit=1) or False
        }
