from odoo import api, Command, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _name = 'project.project'
    _description = 'Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, id'
    _check_company_auto = True
    _rec_name = 'name_to_show'

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['project.stage'].search([], order=order)

    @api.model
    def _search_is_favorite(self, operator, value):
        if operator not in ['=', '!='] or not isinstance(value, bool):
            raise NotImplementedError(_('Operation not supported'))
        return [('favorite_user_ids', 'in' if (operator == '=') == value else 'not in', self.env.uid)]

    def _get_default_stage_id(self):
        return self.env['project.stage'].search([
            ('fold', '=', False),
            '|', ('company_ids', '=', False), ('company_ids', 'in', [self.env.company.id])
        ], limit=1)

    code = fields.Char(string='Code', copy=False, default=lambda self: _('New'), readonly=True, required=True)
    name = fields.Char(string='Name', index='trigram', required=True, tracking=True, translate=True,
                       help='Name of your project. It can be anything you want e.g. the name of a customer or a service.')
    description = fields.Html(string='Description',
                              help='Description to provide more information and context about this project.')
    active = fields.Boolean('Active', default=True, tracking=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency', readonly=True)
    color = fields.Integer(string='Color')
    stage_id = fields.Many2one('project.stage', string='Stage', copy=True, default=_get_default_stage_id,
                               domain="['|', ('company_ids', '=', False), ('company_ids', 'in', company_id)]",
                               group_expand='_read_group_stage_ids', index=True, ondelete='restrict', required=True,
                               tracking=True)
    project_member_ids = fields.One2many('project.member', 'project_id', string='Project Team', copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', copy=True,
                                 domain="[('is_company', '=', True)]", ondelete='restrict', required=True,
                                 tracking=True)
    project_manager_id = fields.Many2one('hr.employee', string='Project Manager', compute='_compute_project_manager_id',
                                         inverse='_inverse_project_manager_id', check_company=True, copy=True,
                                         domain="[('company_id', '=', company_id)]", required=False, store=True,
                                         tracking=True)
    date_start = fields.Date(string='Start Date', default=fields.Date.today, required=True)
    date_end = fields.Date(string='Expiration Date', index=True, required=True, tracking=True,
                           help='Date on which this project ends. The timeframe defined on the project is taken into account when viewing its planning.')
    tag_ids = fields.Many2many('project.tag', relation='project_project_tag_rel', column1='project_id',
                               column2='tag_id', string='Project Tags')
    favorite_user_ids = fields.Many2many('res.users', relation='project_favorite_user_rel', column1='project_id',
                                         column2='user_id', string='Favorite Of', copy=False)
    is_favorite = fields.Boolean(compute='_compute_is_favorite', compute_sudo=True, readonly=False,
                                 search='_search_is_favorite')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', copy=False,
                                          check_company=True,
                                          domain="['|', ('company_id', '=', False), ('company_id', '=?', company_id)]",
                                          ondelete='set null')
    task_ids = fields.One2many('task.task', 'parent_ref_id', string='Tasks',
                               domain=lambda self: [('parent_ref_type', '=', self._name)])
    name_to_show = fields.Char(string='name_to_show', compute='_get_name_to_show')
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks Count')
    milestone_count = fields.Integer(compute='_compute_milestone_count', string='Milestones Count')
    can_edit = fields.Boolean(compute='_compute_can_edit', default=True)

    _sql_constraints = [
        ('project_date_end_greater', 'check(date_end >= date_start)', "The project's start date must be before its end date.")
    ]

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('date_start', 'date_end', 'project_member_ids')
    def _check_member_date_range(self):
        for rec in self.mapped('project_member_ids'):
            if not rec.project_id.date_start <= rec.date_start <= rec.project_id.date_end or \
                    not rec.project_id.date_start <= rec.date_end <= rec.project_id.date_end:
                raise ValidationError(_("The participation period in the project of '%s' must be in project's dates",
                                        rec.employee_id.name))

    @api.constrains('date_start', 'date_end')
    def _check_tasks_date_range(self):
        for rec in self.mapped('task_ids'):
            if not rec.project_id.date_start <= fields.Date.to_date(rec.date_deadline) <= rec.project_id.date_end:
                raise ValidationError(_("Deadline date of task order should be in project's dates."))

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('code', 'name')
    def _get_name_to_show(self):
        for rec in self:
            name = (rec.code + ' | ' + (rec.name or ''))
            rec.name_to_show = name

    def _compute_can_edit(self):
        for rec in self:
            rec.can_edit = rec.active and not rec.stage_id.fold

    @api.depends('project_member_ids.role_id')
    def _compute_project_manager_id(self):
        for rec in self:
            rec.project_manager_id = rec.project_member_ids.filtered(lambda t: t.role_id == self.env.ref(
                'project_mngmnt.project_role_project_manager'))[:1].employee_id or False

    @api.onchange('project_manager_id')
    def _inverse_project_manager_id(self):
        for rec in self.filtered(lambda pr: pr.project_manager_id):
            member_team = self.project_member_ids.filtered(lambda t: t.role_id == self.env.ref(
                'project_mngmnt.project_role_project_manager'))[:1]
            if member_team:
                member_team.employee_id = rec.project_manager_id
            else:
                rec.project_member_ids = [Command.create({
                    'role_id': self.env.ref('project_mngmnt.project_role_project_manager').id,
                    'employee_id': rec.project_manager_id.id
                })]

    @api.depends('task_ids')
    def _compute_task_count(self):
        task_data = self.env['task.task']._read_group(
            domain=[
                ('parent_ref_type', '=', self._name),
                ('parent_ref_id', 'in', self.ids),
                ('parent_id', '!=', False)
            ],
            fields=['parent_ref_id'],
            groupby=['parent_ref_id']
        )
        mapped_data = {x['parent_ref_id']: x['parent_ref_id_count'] for x in task_data}
        for rec in self:
            rec.task_count = mapped_data.get(rec.id, 0)

    @api.depends('task_ids')
    def _compute_milestone_count(self):
        task_data = self.env['task.task']._read_group(
            domain=[
                ('parent_ref_type', '=', self._name),
                ('parent_ref_id', 'in', self.ids),
                ('parent_id', '=', False)
            ],
            fields=['parent_ref_id'],
            groupby=['parent_ref_id']
        )
        mapped_data = {x['parent_ref_id']: x['parent_ref_id_count'] for x in task_data}
        for rec in self:
            rec.milestone_count = mapped_data.get(rec.id, 0)

    def _compute_is_favorite(self):
        for rec in self:
            rec.is_favorite = self.env.user in rec.favorite_user_ids

    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------

    @api.onchange('date_end')
    def _onchange_date_end(self):
        if self.date_end:
            self.project_member_ids.filtered(lambda m: not m.date_end).date_end = self.date_end

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('project.project') or _('New')

            if vals.pop('is_favorite', False):
                vals['favorite_user_ids'] = [self.env.uid]
        records = super(Project, self).create(vals_list)
        return records

    def write(self, vals):
        if 'is_favorite' in vals:
            self._set_favorite_user_ids(vals.pop('is_favorite'))

        res = super(Project, self).write(vals)

        if 'name' in vals and self.analytic_account_id:
            self.analytic_account_id.write({'name': self.name})
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _('%s (copy)') % self.name
        result = super(Project, self).copy(default)

        return result

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_tasks(self):
        action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id(
            'project_mngmnt.task_task_action_view_from_project')
        action['display_name'] = _('%(name)s', name=self.name)
        return action

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _set_favorite_user_ids(self, is_favorite):
        self_sudo = self.sudo()
        if is_favorite:
            self_sudo.favorite_user_ids = [Command.link(self.env.user.id)]
        else:
            self_sudo.favorite_user_ids = [Command.unlink(self.env.user.id)]
