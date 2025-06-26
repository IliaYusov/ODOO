from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.account'

    project_ids = fields.One2many('project_budget.projects', 'responsibility_center_id', string='Projects',
                                  compute='_compute_project_ids')
    project_count = fields.Integer(compute='_compute_project_count')

    revenue = fields.Float(string='Revenue', compute='_compute_amounts')
    cost = fields.Float(string='Cost', compute='_compute_amounts')
    margin = fields.Float(string='Margin', compute='_compute_amounts')
    profitability = fields.Float(string='Profitability', compute='_compute_amounts')

    def _compute_project_ids(self):
        for rec in self:
            rec.project_ids = self.env['project_budget.projects'].search([
                ('budget_state', '=', 'work'),
                ('step_status', '=', 'project'),
                ('responsibility_center_id', '=', rec.id)
            ])

    def _compute_project_count(self):
        projects = self.env['project_budget.projects']._read_group([
            ('budget_state', '=', 'work'),
            ('step_status', '=', 'project'),
            ('responsibility_center_id', 'in', self.ids)
        ], ['responsibility_center_id'], ['responsibility_center_id'])
        projects_count = {p['responsibility_center_id'][0]: p['responsibility_center_id_count'] for p in projects}
        for rec in self:
            rec.project_count = projects_count.get(rec.id, 0)

    @api.depends('project_ids')
    def _compute_amounts(self):
        for rec in self:
            rec.revenue = round(sum([pr.amount_untaxed for pr in rec.project_ids]), 2) or 0
            rec.cost = round(sum([pr.cost_price for pr in rec.project_ids]), 2) or 0
            rec.margin = round(sum([pr.margin for pr in rec.project_ids]), 2) or 0
            rec.profitability = rec.margin / rec.revenue if rec.revenue > 0 else 0
