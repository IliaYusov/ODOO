import logging

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import pytz
from datetime import datetime

_logger = logging.getLogger(__name__)


class CommercialBudget(models.Model):
    _name = 'project_budget.commercial_budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "project_commercial budget"
    _rec_name = 'name_to_show'
    _order = 'date_actual desc'

    name = fields.Char(string="commercial_budget name", required=True)
    budget_state = fields.Selection([('work', 'Working'), ('fixed', 'Fixed')], required=True, index=True, default='work', copy = False, tracking=True)
    etalon_budget = fields.Boolean(string="etalon_budget", default = False)
    date_actual = fields.Datetime(string="Actuality date", index=True, copy=False)
    year = fields.Integer(string="Budget year", required=True, index=True,default=2023)
    currency_id = fields.Many2one('res.currency', string='Account Currency')
    descr = fields.Text( string='Description', default="")
    name_to_show = fields.Char(string='name_to_show', compute='_get_name_to_show')
    projects_ids = fields.One2many(
        comodel_name='project_budget.projects',
        inverse_name='commercial_budget_id',
        string="commercial_budget specification",
        copy=False, auto_join=True)

    def _get_name_to_show(self):
        for commercial_budget in self:
            if commercial_budget.date_actual:
                commercial_budget.name_to_show = commercial_budget.name + ' (' + commercial_budget.budget_state + ' ' + commercial_budget.date_actual.strftime("%d-%m-%Y") + ')'
            else:
                commercial_budget.name_to_show = commercial_budget.name + ' (' + commercial_budget.budget_state+')'

    @api.constrains('year')
    def _check_date_end(self):
        for record in self:
            if record.year < 2022 or record.year > 2030:
                raisetext = _("The year must be between 2022-2030")
                raise ValidationError(raisetext)

    def set_budget_fixed(self):
        if not self.user_has_groups('project_budget.project_budget_admin'):
            raisetext = _("Only users in group project_budget.project_budget_admin can set budget to fixed")
            raise (ValidationError(raisetext))
        else:
            if self.budget_state == 'fixed':
                raisetext = _("Only working budget can be duplicated")
            self.ensure_one()
            _logger.info('Fixing The Budget: Time start = %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            newbudget = self.env['project_budget.commercial_budget'].sudo().browse(self.id).copy({
                'budget_state': 'fixed',
                'date_actual': fields.datetime.now(),
            })
            _logger.info('Fixing The Budget: End copy budget = %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # меняем parent_id в скопированных проектах
            child_projects = self.env['project_budget.projects'].sudo().search([
                ('parent_project_id', '!=', False),
                ('commercial_budget_id', '=', newbudget.id)
            ])
            for child_project in child_projects:
                child_project.parent_project_id = (self.env['project_budget.projects'].sudo().search([
                    ('project_id', '=', child_project.parent_project_id.project_id),
                    ('commercial_budget_id', '=', newbudget.id),
                ]))
            _logger.info('Fixing The Budget: End change step link = %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            newbudget.sudo().with_context(form_fix_budget=True).projects_ids.flush_recordset()
            _logger.info(
                'Fixing The Budget: End saving budget to db = %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            self.sudo().with_context(form_fix_budget=True).projects_ids.filtered(
                lambda pr: pr.step_status == 'project' and pr.stage_id.fold and pr.approve_state != '-') \
                .write({'approve_state': '-'})
            self.sudo().with_context(form_fix_budget=True).projects_ids.filtered(
                lambda pr: pr.step_status == 'project' and not pr.stage_id.fold
                    and pr.approve_state != 'need_approve_manager') \
                .write({'approve_state': 'need_approve_manager'})
            self.env.flush_all()
            _logger.info('Fixing The Budget: Time end = %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def set_budget_work(self):
        self.ensure_one()
        working_budgets = self.env['project_budget.commercial_budget'].search([('budget_state', '=', 'work')])
        if len(working_budgets) > 0 :
            raisetext = _("Already exists budget in work!")
            raise (ValidationError(raisetext))
        else:
            if not self.user_has_groups('project_budget.project_budget_admin'):
                raisetext =_("Only users in group project_budget.project_budget_admin can return budget to work")
                raise (ValidationError(raisetext))
            else:
                self.budget_state='work'
                self.date_actual=None
                return False

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}

        result = super(CommercialBudget, self).copy(default=default)
        for rec in self.projects_ids.filtered(lambda pr: pr.step_status == 'project'):
            rec.with_context(form_fix_budget=True).copy({'commercial_budget_id': result.id})

        return result
