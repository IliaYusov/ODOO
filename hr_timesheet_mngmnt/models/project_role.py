from odoo import fields, models


class ProjectRole(models.Model):
    _inherit = 'project.role'

    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    hourly_cost = fields.Monetary(string='Hourly Cost', default=0.0, groups='project_mngmnt.project_group_manager')
