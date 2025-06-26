from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    token = fields.Char(string='Token', config_parameter='partner_dadata.token')
    secret = fields.Char(string='Secret', config_parameter='partner_dadata.secret')
