from odoo import models, _
from odoo.exceptions import ValidationError


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    def write(self, vals):
        if 'state' in vals:
            if self.analytic_account_id:
                project_count = self.env['crossovered.budget'].search_count([
                    ('id', '!=', self.id),
                    ('analytic_account_id', '=', self.analytic_account_id.id),
                    ('state', 'in', ('confirm', 'done'))
                ])
                if project_count > 0:
                    raise ValidationError(
                        _('The budget for the project "%s" already was confirmed.' % self.analytic_account_id.name))

        res = super(CrossoveredBudget, self).write(vals)
        return res
