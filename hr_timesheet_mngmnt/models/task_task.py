from odoo import models, fields, api


class Task(models.Model):
    _inherit = 'task.task'

    allow_timesheets = fields.Boolean(string='Allow Timesheets', compute='_compute_allow_timesheets',
                                      help='Timesheets can be logged on this task.', readonly=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account', compute='_compute_analytic_account_id',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", ondelete='set null',
        readonly=False, store=True,
        help="""Analytic account to which this task and its timesheets are linked.
             Track the costs and revenues of your task by setting its analytic account on your related documents.
             By default, the analytic account of the project is set. However, it can be changed on each task individually if necessary.""")
    effective_hours = fields.Float(string='Hours Spent', compute='_compute_effective_hours', compute_sudo=True,
                                   store=True)
    total_hours_spent = fields.Float(string='Total Hours', compute='_compute_total_hours_spent', store=True,
                                     help='Time spent on this task and its sub-tasks (and their own sub-tasks).')
    subtask_effective_hours = fields.Float(string='Sub-tasks Hours Spent', compute='_compute_subtask_effective_hours',
                                           recursive=True, store=True,
                                           help='Time spent on the sub-tasks (and their own sub-tasks) of this task.')
    timesheet_ids = fields.One2many('account.analytic.line', 'task_id', string='Timesheets')

    @api.depends('project_id', 'project_id.allow_timesheets')
    def _compute_allow_timesheets(self):
        for rec in self:
            rec.allow_timesheets = rec.project_id.allow_timesheets if rec.project_id else False

    @api.depends('project_id', 'project_id.allow_timesheets', 'project_id.analytic_account_id')
    def _compute_analytic_account_id(self):
        for rec in self:
            rec.analytic_account_id = rec.project_id.analytic_account_id if rec.project_id else False

    @api.depends('timesheet_ids.unit_amount')
    def _compute_effective_hours(self):
        if not any(self._ids):
            for rec in self:
                rec.effective_hours = sum(rec.timesheet_ids.mapped('unit_amount'))
            return
        group_data = self.env['account.analytic.line'].read_group(
            domain=[('task_id', 'in', self.ids)],
            fields=['unit_amount', 'task_id'],
            groupby=['task_id']
        )
        mapped_data = {res['task_id'][0]: res['unit_amount'] for res in group_data}
        for rec in self:
            rec.effective_hours = mapped_data.get(rec.id, 0.0)

    @api.depends('effective_hours', 'subtask_effective_hours')
    def _compute_total_hours_spent(self):
        for rec in self:
            rec.total_hours_spent = rec.effective_hours + rec.subtask_effective_hours

    @api.depends('child_ids.effective_hours', 'child_ids.subtask_effective_hours')
    def _compute_subtask_effective_hours(self):
        for rec in self.with_context(active_test=False):
            rec.subtask_effective_hours = sum(
                child_task.effective_hours + child_task.subtask_effective_hours for child_task in rec.child_ids)
