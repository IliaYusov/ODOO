from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    opportunity_id = fields.Many2one('project_budget.projects', string='Opportunity', depends=['partner_id'],
                                     domain="[('budget_state', '=', 'work'), ('step_status', '=', 'project'), ('partner_id', '=', partner_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                     groups='project_budget.project_budget_users,project_budget.project_budget_admin',
                                     tracking=True)

    profitable_contract_id = fields.Many2one('contract.contract', related='opportunity_id.profitable_contract_id')
