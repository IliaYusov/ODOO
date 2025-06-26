from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.project_budget.models.project_budget_flow_mixin import FlowMixin


class PlannedAcceptanceFlow(models.Model):
    _inherit = 'project_budget.planned_acceptance_flow'

    # NOTE: смысла в поле нет, необходимо для проекта по дашбордам, коллеги построили на нем аналитику, не удалять!!!
    date_actual = fields.Datetime(related='projects_id.date_actual', readonly=True)


class FactAcceptanceFlow(models.Model):
    _inherit = 'project_budget.fact_acceptance_flow'

    planned_acceptance_flow_id = fields.Many2one('project_budget.planned_acceptance_flow', index=True, copy=False,
                                                 store=True, string='Planned Acceptance Flow',
                                                 domain="[('projects_id', '=', projects_id), ('currency_id', '=', currency_id), ('distribution_acceptance_ids', '=', False)]")
    margin = fields.Monetary(string='Margin', compute='_compute_margin', copy=True, readonly=False, store=True)
    margin_in_company_currency = fields.Monetary(string='Margin In Company Currency',
                                                 compute='_compute_margin_in_company_currency', copy=True, store=True)
    margin_manual_input = fields.Boolean(string='Manual input of margin', default=False, copy=True)

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('planned_acceptance_flow_id')
    def _check_one_plan_for_one_fact(self):
        for rec in self:
            if not rec.env.context.get('form_fix_budget'):
                if self.env['project_budget.fact_acceptance_flow'].search_count([
                    ('planned_acceptance_flow_id', '=', rec.planned_acceptance_flow_id.id),
                    ('planned_acceptance_flow_id', '!=', False)
                ], limit=2) > 1:
                    raise_text = _('Acceptance forecast {0} is assigned to several facts')
                    raise_text = raise_text.format(rec.planned_acceptance_flow_id.flow_id)
                    raise ValidationError(raise_text)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('amount', 'margin_manual_input', 'projects_id.profitability', 'step_project_child_id.profitability')
    def _compute_margin(self):
        for rec in self:
            if not rec.margin_manual_input:
                if rec.project_have_steps:
                    rec.margin = rec.amount * rec.step_project_child_id.profitability / 100
                else:
                    rec.margin = rec.amount * rec.projects_id.profitability / 100

    @api.depends('margin', 'currency_rate')
    def _compute_margin_in_company_currency(self):
        for rec in self:
            rec.margin_in_company_currency = rec.margin * rec.currency_rate

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        records = super(FactAcceptanceFlow, self).create(vals_list)
        if not self.env.context.get('form_fix_budget'):
            for rec in records:
                if rec['planned_acceptance_flow_id']:
                    self.env['project_budget.distribution_acceptance'].create({
                        'fact_acceptance_flow_id': rec.id,
                        'planned_acceptance_flow_id': rec.planned_acceptance_flow_id.id,
                        'amount': rec.amount,
                    })
        return records

    def write(self, vals):
        if not self.env.context.get('form_fix_budget'):
            if vals.get('planned_acceptance_flow_id'):
                distribution = self.env['project_budget.distribution_acceptance'].search([
                    ('planned_acceptance_flow_id', '=', vals['planned_acceptance_flow_id'])
                ], limit=1)

                if distribution:
                    distribution.amount = vals.get('amount', 0)
                else:
                    self.env['project_budget.distribution_acceptance'].search([
                        ('fact_acceptance_flow_id', '=', self.id)
                    ]).unlink()
                    self.env['project_budget.distribution_acceptance'].create({
                        'fact_acceptance_flow_id': self.id,
                        'planned_acceptance_flow_id': vals['planned_acceptance_flow_id'],
                        'amount': vals.get('amount', self.amount)
                    })
            elif 'amount' in vals and self.planned_acceptance_flow_id:
                distribution = self.env['project_budget.distribution_acceptance'].search([
                    ('fact_acceptance_flow_id', '=', self.id)
                ], limit=1)
                if distribution:
                    distribution.amount = vals['amount']
            elif 'planned_acceptance_flow_id' in vals and not vals['planned_acceptance_flow_id']:
                self.env['project_budget.distribution_acceptance'].search([
                    ('fact_acceptance_flow_id', '=', self.id)
                ]).unlink()
        res = super(FactAcceptanceFlow, self).write(vals)
        return res

    # ------------------------------------------------------
    # FLOW MIXIN
    # ------------------------------------------------------

    def action_copy_flow(self):
        FlowMixin.action_copy_flow(self, {'distribution_acceptance_ids': None, 'planned_acceptance_flow_id': False})
