from odoo import api, fields, models, _


class Project(models.Model):
    _inherit = 'project.project'

    planned_amount_total = fields.Monetary(string='Total Planned Amount', compute='_compute_budget',
                                           groups='project_mngmnt.project_group_project_manager')
    practical_amount_total = fields.Monetary(string='Total Practical Amount', compute='_compute_budget',
                                             groups='project_mngmnt.project_group_project_manager')
    budget_spent_progress = fields.Monetary(compute='_compute_budget',
                                            groups='project_mngmnt.project_group_project_manager')

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('analytic_account_id')
    def _compute_budget(self):
        budget_lines = self.env['crossovered.budget.line'].search([
            ('analytic_account_id', 'in', self.analytic_account_id.ids),
            ('crossovered_budget_state', 'in', ('confirm', 'done'))
        ])
        for rec in self:
            budget_data = budget_lines.filtered(lambda l: l.analytic_account_id.id == rec.analytic_account_id.id)
            rec.planned_amount_total = sum(
                budget_data.filtered(lambda l: l.general_budget_id.direction == 'income').mapped(
                    'planned_amount_in_budget_currency')) or 0.0
            rec.practical_amount_total = sum(
                budget_data.filtered(lambda l: l.general_budget_id.direction == 'expense').mapped(
                    'practical_amount')) or 0.0
            rec.budget_spent_progress = rec.planned_amount_total and (
                rec.planned_amount_total - rec.practical_amount_total) / rec.planned_amount_total

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_budgets(self):
        self.ensure_one()
        action_vals = {
            'name': _('Budgets'),
            'type': 'ir.actions.act_window',
            'res_model': 'crossovered.budget',
            'view_mode': 'tree,form',
            'domain': [
                ('analytic_account_id', '=', self.analytic_account_id.id)
            ],
            'context': {
                'default_name': _("Budget '%s'" % self.name),
                'default_analytic_account_id': self.analytic_account_id.id,
                'default_responsible_id': self.project_manager_id.user_id.id,
                'default_date_from': self.date_start,
                'default_date_to': self.date_end
            }
        }
        return action_vals
