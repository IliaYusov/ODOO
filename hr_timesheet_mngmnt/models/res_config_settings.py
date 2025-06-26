from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    timesheet_account_id = fields.Many2one(related='company_id.timesheet_account_id', readonly=False)
