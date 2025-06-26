from odoo import api, fields, models, _


class PlannedCashFlow(models.Model):
    _name = 'project_budget.planned_cash_flow'
    _description = 'Planned Cash Flow'
    _inherit = ['project_budget.flow.mixin']

    flow_id = fields.Char(string='Flow Id', copy=True, default='-', index=True, readonly=True, required=True)
    distribution_cash_ids = fields.One2many('project_budget.distribution_cash', 'planned_cash_flow_id',
                                            string='Distribution Fact By Plan', copy=False)
    amount_distribution = fields.Monetary(string='Distribution Amount', compute='_compute_amount', copy=True,
                                          precompute=True, store=True)
    amount_distribution_in_company_currency = fields.Monetary(string='Distribution Amount In Company Currency',
                                                              compute='_compute_amount', copy=True,
                                                              currency_field='company_currency_id', precompute=True,
                                                              store=True)
    amount_remaining = fields.Monetary(string='Remaining Amount', compute='_compute_amount', copy=True,
                                       precompute=True, store=True)
    amount_remaining_in_company_currency = fields.Monetary(string='Remaining Amount In Company Currency',
                                                           compute='_compute_amount', copy=True,
                                                           currency_field='company_currency_id', precompute=True,
                                                           store=True)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('amount', 'currency_rate', 'distribution_cash_ids.amount',
                 'distribution_cash_ids.amount_in_company_currency')
    def _compute_amount(self):
        for rec in self:
            rec.amount_distribution = sum(rec.distribution_cash_ids.mapped('amount'))
            rec.amount_distribution_in_company_currency = sum(
                rec.distribution_cash_ids.mapped('amount_in_company_currency'))
            rec.amount_remaining = rec.amount - sum(rec.distribution_cash_ids.mapped('amount'))
            rec.amount_remaining_in_company_currency = 0 if rec.amount_remaining == 0 else \
                rec.amount_in_company_currency - sum(rec.distribution_cash_ids.mapped('amount_in_company_currency'))

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('flow_id') or vals['flow_id'] == '-':
                vals['flow_id'] = self.env['ir.sequence'].sudo().next_by_code('project_budget.planned_cash_flow')
        return super().create(vals_list)

    # ------------------------------------------------------
    # CORE METHODS OVERRIDES
    # ------------------------------------------------------

    def name_get(self):
        result = []
        for rec in self:
            name = rec.date.strftime('%d/%m/%Y') + _(' | cash ') + rec.flow_id + _(' | sum cash') + f'{rec.amount:_.2f}'
            if rec.project_have_steps:
                name += _(' | step ') + (rec.step_project_child_id.project_id or '') + _(' | code ') + (
                        rec.step_project_child_id.step_project_number or '') + _(' | essence_project ') + (
                                rec.step_project_child_id.essence_project or '')
            result.append((rec.id, name))
        return result

    # ------------------------------------------------------
    # FLOW MIXIN
    # ------------------------------------------------------

    def action_copy_flow(self):
        super(PlannedCashFlow, self).action_copy_flow({'flow_id': '-'})


class FactCashFlow(models.Model):
    _name = 'project_budget.fact_cash_flow'
    _description = 'Fact Cash Flow'
    _inherit = ['project_budget.flow.mixin']

    currency_rate = fields.Float(readonly=False)
    distribution_cash_ids = fields.One2many('project_budget.distribution_cash', 'fact_cash_flow_id',
                                            string='Distribution Fact By Plan', copy=False)
    amount_distribution = fields.Monetary(string='Distribution Amount', compute='_compute_amount', copy=True,
                                          precompute=True, store=True)
    amount_distribution_in_company_currency = fields.Monetary(string='Distribution Amount In Company Currency',
                                                              compute='_compute_amount', copy=True,
                                                              currency_field='company_currency_id', precompute=True,
                                                              store=True)
    amount_remaining = fields.Monetary(string='Remaining Amount', compute='_compute_amount', copy=True,
                                       precompute=True, store=True)
    amount_remaining_in_company_currency = fields.Monetary(string='Remaining Amount In Company Currency',
                                                           compute='_compute_amount', copy=True,
                                                           currency_field='company_currency_id', precompute=True,
                                                           store=True)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('amount', 'distribution_cash_ids.amount', 'distribution_cash_ids.amount_in_company_currency')
    def _compute_amount(self):
        for rec in self:
            rec.amount_distribution = sum(rec.distribution_cash_ids.mapped('amount'))
            rec.amount_distribution_in_company_currency = sum(
                rec.distribution_cash_ids.mapped('amount_in_company_currency'))
            rec.amount_remaining = rec.amount - rec.amount_distribution
            rec.amount_remaining_in_company_currency = 0 if rec.amount_remaining == 0 else \
                rec.amount_in_company_currency - rec.amount_distribution_in_company_currency

    # ------------------------------------------------------
    # FLOW MIXIN
    # ------------------------------------------------------

    def action_copy_flow(self):
        super(FactCashFlow, self).action_copy_flow({'distribution_cash_ids': None})
