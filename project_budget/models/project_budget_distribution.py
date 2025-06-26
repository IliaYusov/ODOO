from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DistributionAcceptance(models.Model):
    _name = 'project_budget.distribution_acceptance'
    _description = 'Distribution Acceptance Fact By Plan'

    fact_acceptance_flow_id = fields.Many2one('project_budget.fact_acceptance_flow', string='Fact Acceptance Flow',
                                              copy=True, domain="[('projects_id', '=', parent.projects_id)]",
                                              index=True, ondelete='cascade', required=True)
    fact_currency_id = fields.Many2one(related='fact_acceptance_flow_id.currency_id', readonly=True)
    currency_rate = fields.Float(related='fact_acceptance_flow_id.currency_rate', readonly=True)

    planned_acceptance_flow_id = fields.Many2one('project_budget.planned_acceptance_flow',
                                                 string='Planned Acceptance Flow', copy=True,
                                                 domain="[('projects_id', '=', parent.projects_id), ('currency_id', '=', fact_currency_id)]",
                                                 index=True, ondelete='cascade', required=True)
    plan_currency_id = fields.Many2one(related='planned_acceptance_flow_id.currency_id', readonly=True)
    company_currency_id = fields.Many2one(related='planned_acceptance_flow_id.company_currency_id', readonly=True)
    amount_plan = fields.Monetary(related='planned_acceptance_flow_id.amount', string='Planned Amount',
                                  currency_field='plan_currency_id', readonly=True)
    amount_plan_in_company_currency = fields.Monetary(related='planned_acceptance_flow_id.amount_in_company_currency',
                                                      string='Planned Amount In Company Currency',
                                                      currency_field='company_currency_id', readonly=True)
    amount_remaining = fields.Monetary(related='planned_acceptance_flow_id.amount_remaining',
                                       currency_field='plan_currency_id', readonly=True)

    amount = fields.Monetary(string='Amount', copy=True, currency_field='fact_currency_id', required=True)
    amount_in_company_currency = fields.Monetary(string='Amount In Company Currency',
                                                 compute='_compute_amount_in_company_currency',
                                                 currency_field='company_currency_id', precompute=True, store=True)

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('plan_currency_id', 'fact_currency_id')
    def _check_currency_id(self):
        for rec in self:
            if rec.fact_currency_id != rec.plan_currency_id:
                raise ValidationError(_('The currency of plan and fact must match!'))

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('amount', 'currency_rate')
    def _compute_amount_in_company_currency(self):
        for rec in self:
            if rec.fact_currency_id == rec.company_currency_id:
                rec.amount_in_company_currency = rec.amount
            else:
                rec.amount_in_company_currency = rec.amount * rec.currency_rate

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    @api.onchange('planned_acceptance_flow_id')
    def _onchange_planned_acceptance_flow_id(self):
        if self.planned_acceptance_flow_id.ids:
            distribution = {}
            distributions = [distribution for distribution in self.fact_acceptance_flow_id.distribution_acceptance_ids
                             if hasattr(distribution.id, 'origin') and distribution.id.origin is not False]
            for distr in distributions[:-1]:
                distribution['total'] = distribution.get('total', 0) + distr.amount
                if distr.id.origin is None:
                    distribution[distr.planned_acceptance_flow_id] = distribution.get(distr.planned_acceptance_flow_id,
                                                                                      0) + distr.amount
            self.amount = min(self.amount_remaining - distribution.get(self.planned_acceptance_flow_id, 0),
                              self.fact_acceptance_flow_id.amount - distribution.get('total', 0))


class CashFlowDistribution(models.Model):
    _name = 'project_budget.distribution_cash'
    _description = 'Distribution Cash Flow Fact By Plan'

    fact_cash_flow_id = fields.Many2one('project_budget.fact_cash_flow', string='Fact Cash Flow', copy=True,
                                        domain="[('projects_id', '=', parent.projects_id)]", index=True,
                                        ondelete='cascade', required=True)
    fact_currency_id = fields.Many2one(related='fact_cash_flow_id.currency_id', readonly=True)
    currency_rate = fields.Float(related='fact_cash_flow_id.currency_rate', readonly=True)

    planned_cash_flow_id = fields.Many2one('project_budget.planned_cash_flow', string='Planned Cash Flow', copy=True,
                                           domain="[('projects_id', '=', parent.projects_id), ('currency_id', '=', fact_currency_id)]",
                                           index=True, ondelete='cascade', required=True)
    plan_currency_id = fields.Many2one(related='planned_cash_flow_id.currency_id', readonly=True)
    company_currency_id = fields.Many2one(related='planned_cash_flow_id.company_currency_id', readonly=True)
    amount_plan = fields.Monetary(related='planned_cash_flow_id.amount', string='Planned Amount',
                                  currency_field='plan_currency_id', readonly=True)
    amount_plan_in_company_currency = fields.Monetary(related='planned_cash_flow_id.amount_in_company_currency',
                                                      string='Planned Amount In Company Currency',
                                                      currency_field='company_currency_id', readonly=True)
    amount_remaining = fields.Monetary(related='planned_cash_flow_id.amount_remaining',
                                       currency_field='plan_currency_id', readonly=True)

    amount = fields.Monetary(string='Amount', copy=True, currency_field='fact_currency_id', required=True)
    amount_in_company_currency = fields.Monetary(string='Amount In Company Currency',
                                                 compute='_compute_amount_in_company_currency', copy=True,
                                                 currency_field='company_currency_id', precompute=True, store=True)
    factoring = fields.Boolean(string='Factoring', default=False)

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('plan_currency_id', 'fact_currency_id')
    def _check_currency_id(self):
        for rec in self:
            if rec.fact_currency_id != rec.plan_currency_id:
                raise ValidationError(_('The currency of plan and fact must match!'))

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('amount', 'currency_rate')
    def _compute_amount_in_company_currency(self):
        for rec in self:
            if rec.fact_currency_id == rec.company_currency_id:
                rec.amount_in_company_currency = rec.amount
            else:
                rec.amount_in_company_currency = rec.amount * rec.currency_rate

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    @api.onchange('planned_cash_flow_id')
    def _onchange_planned_cash_flow_id(self):
        if self.planned_cash_flow_id.ids:
            distribution = {}
            distributions = [distribution for distribution in self.fact_cash_flow_id.distribution_cash_ids
                             if hasattr(distribution.id, 'origin') and distribution.id.origin is not False]
            for distr in distributions[:-1]:
                distribution['total'] = distribution.get('total', 0) + distr.amount
                if distr.id.origin is None:
                    distribution[distr.planned_cash_flow_id] = distribution.get(distr.planned_cash_flow_id,
                                                                                0) + distr.amount
            if self.fact_cash_flow_id.amount >= 0:
                self.amount = min(
                    max(self.amount_remaining - distribution.get(self.planned_cash_flow_id, 0), 0),
                    max(self.fact_cash_flow_id.amount - distribution.get('total', 0), 0)
                )
            else:  # если факт отрицательный, то берем большее из чисел, но не положительное
                self.amount = max(
                    min(self.amount_remaining - distribution.get(self.planned_cash_flow_id, 0), 0),
                    min(self.fact_cash_flow_id.amount - distribution.get('total', 0), 0)
                )
