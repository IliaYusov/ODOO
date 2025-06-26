from odoo import models, _
from odoo.exceptions import UserError
from ..tools import dadata


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_update_info_by_vat(self):
        partners_info = self._get_partners_info()
        for rec in self:
            rec.write(partners_info.get(rec.id))

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _get_partners_info(self):
        result = dict()
        for rec in self:
            partner_info = dadata.get_partner_info_by_vat(self.env, rec.vat)
            if not partner_info:
                raise UserError(_('Organization not found. Please check Tax ID.'))
            result[rec.id] = {
                'id': rec.id,
                'name': partner_info.get('name') or partner_info.get('full_name'),
                'full_name': partner_info.get('full_name'),
                'street': partner_info.get('street'),
                'city': partner_info.get('city'),
                'zip': partner_info.get('zip'),
                'country_id': partner_info.get('country_id', False)
            }
        return result
