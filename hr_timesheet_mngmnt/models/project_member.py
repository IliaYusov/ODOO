from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class ProjectMember(models.Model):
    _inherit = 'project.member'

    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    hourly_cost = fields.Monetary(
        string='Hourly Cost', compute='_compute_hourly_cost', readonly=False, store=True,
        groups='project_mngmnt.project_group_manager'
    )

    # ------------------------------------------------------
    # COMPUTES
    # ------------------------------------------------------

    @api.depends('employee_id', 'role_id', 'project_id.manual_hourly_cost')
    def _compute_hourly_cost(self):
        for rec in self:
            if not rec.project_id.manual_hourly_cost:
                rec.hourly_cost = rec._hourly_cost()

    def _hourly_cost(self):
        self.ensure_one()
        locals_dict = {
            'record': self
        }
        try:
            safe_eval(self.project_id.account_method_employee_rate_id.expression, locals_dict, mode='exec', nocopy=True)
            result = locals_dict.get('result', 0.0)
        except Warning as ex:
            raise ex
        except SyntaxError as ex:
            raise UserError(_('Wrong python code defined.\n\nError: %s\nLine: %s, Column: %s\n\n%s' % (
                ex.args[0], ex.args[1][1], ex.args[1][2], ex.args[1][3])))
        return result