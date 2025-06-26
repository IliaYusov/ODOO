from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    full_name = fields.Char(string='Full Name')
