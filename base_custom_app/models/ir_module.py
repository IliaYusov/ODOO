from odoo import api, models


class IrModule(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def is_module_installed(self, name):
        return self.env['ir.module.module'].sudo().search_count([
            ('state', '=', 'installed'),
            ('name', '=', name)
        ]) > 0
