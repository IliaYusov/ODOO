from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        result['show_documentation'] = self.env['ir.module.module'].sudo().search_count([
            ('state', '=', 'installed'),
            ('name', '=', 'knowledge_base')
        ]) > 0
        return result
