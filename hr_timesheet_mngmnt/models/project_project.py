from odoo import api, fields, models, _


class Project(models.Model):
    _inherit = 'project.project'

    allow_timesheets = fields.Boolean(string='Allow Timesheets', copy=True, default=False)
    analytic_account_id = fields.Many2one('account.analytic.account', domain="""[
        '|', ('company_id', '=', False), ('company_id', '=', company_id)], ('partner_id', '=?', partner_id)""")
    account_method_employee_rate_id = fields.Many2one('project.account.method.employee.rate',
                                                      string='Account Method Employee Rate', copy=True,
                                                      ondelete='restrict')
    currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    hourly_cost = fields.Monetary(string='Hourly Cost', copy=True, default=0.0,
                                  groups='project_mngmnt.project_group_project_manager')

    timesheet_ids = fields.One2many('account.analytic.line', 'project_id', string='Timesheets')
    total_hours_spent = fields.Float(compute='_compute_total_hours_spent', string='Hours')
    planned_hours = fields.Float(string='Planned Hours')
    remaining_hours = fields.Float(string='Remaining Invoiced Time', compute='_compute_remaining_hours',
                                   compute_sudo=True)
    is_project_overtime = fields.Boolean(string='Project in Overtime', compute='_compute_remaining_hours',
                                         compute_sudo=True)

    _sql_constraints = [
        ('account_method_employee_rate_id',
         'CHECK(allow_timesheets = true AND account_method_employee_rate_id IS NOT NULL)',
         'Employee rate account method is required for a project.')
    ]

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('timesheet_ids')
    def _compute_total_hours_spent(self):
        group_data = self.env['account.analytic.line'].read_group(
            [('project_id', 'in', self.ids)],
            ['unit_amount', 'project_id'],
            ['project_id'],
            lazy=False
        )
        mapped_data = {res['project_id'][0]: res['unit_amount'] for res in group_data}
        for rec in self:
            rec.total_hours_spent = mapped_data.get(rec.id, 0.0)

    @api.depends('allow_timesheets', 'timesheet_ids')
    def _compute_remaining_hours(self):
        group_data = self.env['account.analytic.line']._read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'unit_amount'],
            ['project_id'],
            lazy=False)
        mapped_data = {res['project_id'][0]: res['unit_amount'] for res in group_data}
        for rec in self:
            rec.remaining_hours = rec.planned_hours - mapped_data.get(rec.id, 0)
            rec.is_project_overtime = rec.remaining_hours < 0

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        defaults = self.default_get(['allow_timesheets', 'analytic_account_id'])
        for vals in vals_list:
            allow_timesheets = vals.get('allow_timesheets', defaults.get('allow_timesheets'))
            analytic_account_id = vals.get('analytic_account_id', defaults.get('analytic_account_id'))
            if allow_timesheets and not analytic_account_id:
                analytic_account = self._create_analytic_account_from_values(vals)
                vals['analytic_account_id'] = analytic_account.id
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('allow_timesheets', False) and not vals.get('analytic_account_id', False):
            [rec._create_analytic_account() for rec in
             self.filtered(lambda pr: not pr.analytic_account_id)]
        return super(Project, self).write(vals)

    @api.model
    def _init_data_analytic_account(self):
        self.search([
            ('allow_timesheets', '=', True),
            ('analytic_account_id', '=', False)
        ])._create_analytic_account()

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_recalc_planned_hours_by_milestones(self):
        self.ensure_one()
        planned_hours = sum(self.task_ids.filtered(lambda t: not t.root_task_id).mapped('planned_hours'))
        self.write({'planned_hours': planned_hours})

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    @api.model
    def _create_analytic_account_from_values(self, values):
        company = self.env['res.company'].browse(values.get('company_id')) if values.get(
            'company_id') else self.env.company
        res_partner = self.env['res.partner'].browse(values.get('partner_id', 0))
        analytic_account = self.env['account.analytic.account'].create({
            'name': values.get('name', _('Unknown Analytic Account')),
            'company_id': company.id,
            'partner_id': res_partner.id or False,
            'plan_id': company.analytic_plan_id.id,
        })
        return analytic_account

    def _create_analytic_account(self):
        for rec in self:
            analytic_account = self.env['account.analytic.account'].create({
                'name': rec.name,
                'company_id': rec.company_id.id,
                'partner_id': rec.partner_id.id,
                'plan_id': rec.company_id.analytic_plan_id.id,
                'active': True
            })
            rec.write({'analytic_account_id': analytic_account.id})
