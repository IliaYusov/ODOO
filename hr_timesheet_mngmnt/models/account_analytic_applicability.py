from odoo import fields, models


class AccountAnalyticApplicability(models.Model):
    _inherit = 'account.analytic.applicability'

    business_domain = fields.Selection(selection_add=[('timesheet', 'Timesheet')], ondelete={'timesheet': 'cascade'})
