from odoo import fields, models


class Contract(models.Model):
    _inherit = 'contract.contract'

    project_id = fields.Many2one('project_budget.projects', string='Project', copy=True,
                                 domain="[('budget_state', '=', 'work'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 tracking=True)
    project_member_ids = fields.One2many('project_budget.project.member', related='project_id.project_member_ids', string='Members')
