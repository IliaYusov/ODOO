from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_partner_dadata = fields.Boolean('Find a company by VAT')
