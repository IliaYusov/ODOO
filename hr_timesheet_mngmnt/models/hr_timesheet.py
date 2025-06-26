from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def default_get(self, field_list):
        result = super(AccountAnalyticLine, self).default_get(field_list)
        if not self.env.context.get('default_employee_id') and 'employee_id' in field_list and result.get('user_id'):
            result['employee_id'] = self.env['hr.employee'].search([
                ('user_id', '=', result['user_id']),
                ('company_id', '=', result.get('company_id', self.env.company.id))
            ], limit=1).id
        return result

    def _domain_employee_id(self):
        domain = [
            '|', ('company_id', '=', False), ('company_id', 'in', self.env.context.get('allowed_company_ids', []))]
        if not self.user_has_groups('hr_timesheet_mngmnt.hr_timesheet_group_manager'):
            domain.append(('user_id', '=', self.env.user.id))
        return domain

    task_id = fields.Many2one('task.task', string='Task',
                              domain="[('parent_ref_type', '=', 'project.project')]", index='btree_not_null',
                              readonly=False, store=True)
    project_id = fields.Many2one('project.project', string='Project', compute='_compute_project_id', index=True,
                                 store=True)
    milestone_id = fields.Many2one('task.task', string='Milestone', compute='_compute_milestone_id', store=True)
    user_id = fields.Many2one('res.users', compute='_compute_user_id', store=True, readonly=False)
    employee_id = fields.Many2one('hr.employee', string='Employee', check_company=True, context={'active_test': False},
                                  domain=_domain_employee_id)
    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_department_id',
                                    compute_sudo=True, store=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', related='employee_id.parent_id', store=True)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('task_id', 'task_id.project_id')
    def _compute_project_id(self):
        for rec in self:
            rec.project_id = rec.task_id.project_id

    @api.depends('employee_id')
    def _compute_user_id(self):
        for rec in self:
            rec.user_id = rec.employee_id.user_id if rec.employee_id else self._default_user()

    @api.depends('employee_id')
    def _compute_department_id(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id

    @api.depends('task_id')
    def _compute_milestone_id(self):
        for rec in self:
            rec.milestone_id = rec.task_id.root_task_id

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = '/'

            vals.update(self._timesheet_preprocess_values(vals))

            if not vals.get('general_account_id'):
                vals['general_account_id'] = self.env['res.company'].browse(
                    vals.get('company_id', self.env.company.id)).timesheet_account_id.id or False

        records = super(AccountAnalyticLine, self).create(vals_list)

        for rec, vals in zip(records, vals_list):
            if rec.project_id:
                rec._timesheet_postprocess(vals)
        return records

    def write(self, vals):
        vals = self._timesheet_preprocess_values(vals)
        result = super(AccountAnalyticLine, self).write(vals)
        self.filtered(lambda t: t.project_id)._timesheet_postprocess(vals)
        return result

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _timesheet_preprocess_values(self, vals):
        task = self.env['task.task'].browse(vals.get('task_id', False))

        if task and not vals.get('account_id'):
            vals['account_id'] = task.analytic_account_id.id
            vals['company_id'] = task.analytic_account_id.company_id.id or task.company_id.id

        return vals

    def _timesheet_postprocess(self, vals):
        values = self._timesheet_postprocess_values(vals)
        for rec in self:
            if values[rec.id]:
                rec.write(values[rec.id])
        return values

    def _timesheet_postprocess_values(self, vals):
        result = {i: {} for i in self.ids}
        sudo_self = self.sudo()
        if any(field_name in vals for field_name in ['unit_amount', 'employee_id', 'account_id']):
            for rec in sudo_self:
                cost = rec._hourly_cost()
                amount = rec.unit_amount * cost
                amount_converted = rec.employee_id.currency_id._convert(
                    amount, rec.account_id.currency_id or rec.currency_id, rec.company_id, rec.date)
                result[rec.id].update({
                    'amount': amount_converted
                })
        return result

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

    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)
