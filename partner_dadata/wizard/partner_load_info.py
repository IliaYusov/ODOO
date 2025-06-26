from odoo import api, fields, models, _
from ..tools import dadata


class PartnerLoadInfo(models.TransientModel):
    _name = 'partner.load.info'
    _description = 'Partner Load Info By DaData'

    vat = fields.Char(string='Tax ID', required=True)
    name = fields.Char(string='Name')
    full_name = fields.Char(string='Full Name')
    street = fields.Char(string='Street')
    zip = fields.Char(string='Zip')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')
    is_load = fields.Boolean(default=False)
    is_exists = fields.Boolean(default=False)

    def get_partner_info_by_vat(self):
        partner_info = dadata.get_partner_info_by_vat(self.env, self.vat)
        if partner_info:
            self.is_load = True
            self.name = partner_info.get('name')
            self.full_name = partner_info.get('full_name')
            self.street = partner_info.get('street')
            self.city = partner_info.get('city')
            self.zip = partner_info.get('zip')
            self.country_id = partner_info.get('country_id')
            self.is_exists = self.env['res.partner'].search_count([
                ('vat', '=', self.vat)
            ]) > 0
        return {
            'name': _('Create Partner'),
            'view_mode': 'form',
            'res_model': 'partner.load.info',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': {
                'show_alert': True
            },
            'target': 'new',
        }

    def action_create_partner(self):
        self.ensure_one()
        partner = self.env['res.partner'].create({
            'is_company': True,
            'name': self.name,
            'full_name': self.full_name,
            'vat': self.vat,
            'street': self.street,
            'zip': self.zip,
            'city': self.city,
            'country_id': self.country_id.id
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'type': 'success',
                'message': _('Partner %s was created' % self.name),
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'res.partner',
                    'view_mode': 'form',
                    'res_id': partner.id,
                    'views': [(False, 'form')]
                }
            }
        }
