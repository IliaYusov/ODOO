from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import pytz
from datetime import timedelta


class commercial_budget(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'project_budget.commercial_budget'
    _description = "project_commercial budget"
    name = fields.Char(string="commercial_budget name", required=True)
    etalon_budget = fields.Boolean(string="etalon_budget", default = False)
    budget_state = fields.Selection([('work', 'Working'), ('fixed', 'Fixed')], required=True, index=True, default='work', copy = False, tracking=True)
    date_actual = fields.Datetime(string="Actuality date", index=True, copy=False)
    year = fields.Integer(string="Budget year", required=True, index=True,default=2023)
    currency_id = fields.Many2one('res.currency', string='Account Currency')
    descr = fields.Text( string='Description', default="")
    projects_ids = fields.One2many(
        comodel_name='project_budget.projects',
        inverse_name='commercial_budget_id',
        string="commercial_budget specification",
        copy=True, auto_join=True)

    def isuseradmin(self):
        self.ensure_one()
        return self.env.ref('project_budget.project_budget_admin')

    @api.constrains('year')
    def _check_date_end(self):
        for record in self:
            if record.year < 2022 or record.year > 2030:
                raisetext = _("The year must be between 2022-2030")
                raise ValidationError(raisetext)

    def get_user_datetime(self):
        fmt = "%Y-%m-%d %H:%M:%S"
        tz = pytz.timezone(self.env.user.tz) or pytz.utc
        now_time = fields.datetime.now(tz=tz)
        my_dt = fields.datetime.strptime(now_time.strftime(fmt), fmt)
        return my_dt

    def set_budget_fixed(self):
        if not self.user_has_groups('project_budget.project_budget_admin'):
            raisetext=_("Only users in group project_budget.project_budget_admin can set budget to fixed")
            raise (ValidationError(raisetext))
        else:
            if self.budget_state == 'fixed':
                raisetext = _("Only working budget can be duplicated")
            self.ensure_one()
            # self.budget_state='fixed'
            # self.date_actual = fields.datetime.now()
            cur_datetime = self.get_user_datetime()
            print('cur_datetime=',cur_datetime)
            self.env['project_budget.commercial_budget'].browse(self.id).copy({'budget_state':'fixed'
                                                                              ,'date_actual': fields.datetime.now()
                                                                                })

            for spec in self.projects_ids:
                spec.approve_state = 'need_approve_manager'

            # self.env['project_budget.projects'].search([('project_id', '=', self.id)]).write({'approve_state': 'need_approve_manager'})


            return False

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

class planned_cash_flow(models.Model):
    _name = 'project_budget.planned_cash_flow'
    _description = "planned cash flow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    projects_id = fields.Many2one('project_budget.projects', string='projects_id',index=True)
    project_have_steps = fields.Boolean(string="project have steps", related='projects_id.project_have_steps', readonly=True)
    project_steps_id = fields.Many2one('project_budget.project_steps', string='project_steps_id', index=True)
    date_cash = fields.Date(string="date_cash" , required=True, copy=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', compute='_compute_reference')
    sum_cash = fields.Monetary(string="sum_cash", required=True, copy=True)
    doc_cash = fields.Char(string="doc_cash", required=True, copy=True)
    @ api.depends('projects_id.currency_id')
    def _compute_reference(self):
        for row in self:
            row.currency_id = row.projects_id.currency_id

class planned_acceptance_flow(models.Model):
    _name = 'project_budget.planned_acceptance_flow'
    _description = "planned acceptance flow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    projects_id = fields.Many2one('project_budget.projects', string='projects_id', index=True)
    project_have_steps = fields.Boolean(string="project have steps", related='projects_id.project_have_steps',
                                        readonly=True)
    project_steps_id = fields.Many2one('project_budget.project_steps', string='project_steps_id', index=True)
    date_cash = fields.Date(string="date_cash" , required=True, copy=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', compute='_compute_reference')
    sum_cash = fields.Monetary(string="sum_cash", required=True, copy=True)
    doc_cash = fields.Char(string="doc_cash", required=True, copy=True)
    @ api.depends('projects_id.currency_id')
    def _compute_reference(self):
        for row in self:
            row.currency_id = row.projects_id.currency_id


class fact_cash_flow(models.Model):
    _name = 'project_budget.fact_cash_flow'
    _description = "fact cash flow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    projects_id = fields.Many2one('project_budget.projects', string='projects_id',index=True)
    project_have_steps = fields.Boolean(string="project have steps", related='projects_id.project_have_steps',
                                        readonly=True)
    project_steps_id = fields.Many2one('project_budget.project_steps', string='project_steps_id', index=True)
    date_cash = fields.Date(string="date_cash" , required=True, copy=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', compute='_compute_reference')
    sum_cash = fields.Monetary(string="sum_cash", required=True, copy=True)
    doc_cash = fields.Char(string="doc_cash", required=True, copy=True)
    @ api.depends('projects_id.currency_id')
    def _compute_reference(self):
        for row in self:
            row.currency_id = row.projects_id.currency_id

class fact_acceptance_flow(models.Model):
    _name = 'project_budget.fact_acceptance_flow'
    _description = "fact acceptance flow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    projects_id = fields.Many2one('project_budget.projects', string='projects_id', index=True)
    project_have_steps = fields.Boolean(string="project have steps", related='projects_id.project_have_steps',
                                        readonly=True)
    project_steps_id = fields.Many2one('project_budget.project_steps', string='project_steps_id', index=True)
    date_cash = fields.Date(string="date_cash" , required=True, copy=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', compute='_compute_reference')
    sum_cash = fields.Monetary(string="sum_cash", required=True, copy=True)
    doc_cash = fields.Char(string="doc_cash", required=True, copy=True)
    @ api.depends('projects_id.currency_id')
    def _compute_reference(self):
        for row in self:
            row.currency_id = row.projects_id.currency_id

class project_steps_type(models.Model):
    _name = 'project_budget.project_steps_type'
    _description = "project steps type"
    name = fields.Char(string="name", required=True)

class project_steps(models.Model):
    _name = 'project_budget.project_steps'
    _description = "project steps"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    projects_id = fields.Many2one('project_budget.projects', string='projects_id', index=True)
    name = fields.Char(string="step name", required=True, copy=True)
    date_step = fields.Date(string="step date" , required=True, copy=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency', related='projects_id.currency_id', readonly=True)
    project_steps_type_id = fields.Many2one('project_budget.project_steps_type', string='project steps type', required=True, copy=True)
    vat_attribute_id = fields.Many2one('project_budget.vat_attribute', string='vat_attribute', copy=True, required=True)
    sum_without_vat = fields.Monetary(string="sum without vat", required=True, copy=True)
    sum_with_vat = fields.Monetary(string="sum_cash", compute='_compute_sum', readonly=True)

    @ api.depends('sum_without_vat','vat_attribute_id')
    def _compute_sum(self):
        for row in self:
            row.sum_with_vat = row.sum_without_vat * (1+row.vat_attribute_id.percent/100)


class projects(models.Model):
    _name = 'project_budget.projects'
    _description = "project_office commercial budget projects"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_names_search = ['project_id', 'essence_project']

    def action_canban_view_group(self):
        data = self.env['project_budget.projects'].search()
        return {
            'name': 'Invoices',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project_budget.projects',
            'view_id': False,
            'views': [data],
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window'
        }

    def _get_supervisor_list(self):
        domain = []
        supervisor_access = self.env['project_budget.project_supervisor_access'].search([('user_id.id', '=', self.env.user.id)])
        supervisor_list = []
        for each in supervisor_access:
            supervisor_list.append(each.project_supervisor_id.id)
        if supervisor_list:
            domain = [('id', 'in', supervisor_list)]
            return domain
        return domain

    def _get_manager_access(self):
        return self.env['project_budget.project_manager_access'].search(
            [('user_id.id', '=', self.env.user.id)])

    def _get_manager_list(self):
        domain = []
        manager_access = self._get_manager_access()
        manager_list = []
        for each in manager_access:
            manager_list.append(each.project_manager_id.id)
        if manager_list:
            domain = [('id', 'in', manager_list)]
            return domain
        return domain

    def _get_commercial_budget_list(self):
        domain = [('id', 'in','-1')]
        commercial_budget = self.env['project_budget.commercial_budget'].search([('budget_state', '=', 'work')])
        commercial_budget_list = []
        for each in commercial_budget:
            commercial_budget_list.append(each.id)
        if commercial_budget_list:
            domain = [('id', 'in', commercial_budget_list)]
            return domain
        return domain

    def _get_first_manager_from_access(self):
        manager_access = self._get_manager_access()
        if manager_access:
            return self.env['project_budget.project_manager'].search(
                    [('id', '=', manager_access[0].project_manager_id.id)])
        return None

    project_id = fields.Char(string="Project_ID", required=True, index=True, copy=True,
                             default='ID') #lambda self: self.env['ir.sequence'].sudo().next_by_code('project_budget.projects'))
    specification_state = fields.Selection([('prepare', 'Prepare'), ('production', 'Production'), ('cancel','Canceled')], required=True,
                                           index=True, default='prepare', store=True, copy=True, tracking=True, compute="_compute_specification_state")
    approve_state= fields.Selection([('need_approve_manager', 'need managers approve'), ('need_approve_supervisor', 'need supervisors approve'), ('approved','approved')],
                                    required=True, index=True, default='need_approve_manager', store=True, copy=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency',  compute='_compute_reference')
    etalon_budget = fields.Boolean(string="etalon_budget", compute='_compute_reference')
    commercial_budget_id = fields.Many2one('project_budget.commercial_budget', string='commercial_budget-',required=True, ondelete='cascade', index=True, copy=False
                                           ,default=lambda self: self.env['project_budget.commercial_budget'].search([('budget_state', '=', 'work')], limit=1)
                                           , domain=_get_commercial_budget_list)
    budget_state = fields.Selection([('work', 'Working'), ('fixed', 'Fixed')], required=True, index=True, default='work', copy = False,
                                    compute='_compute_reference', store=True, tracking=True)
    project_office_id = fields.Many2one('project_budget.project_office', string='project_office', required=True,
                                        copy=True)
    project_supervisor_id = fields.Many2one('project_budget.project_supervisor', string='project_supervisor',
                                            required=True, copy=True, domain=_get_supervisor_list, tracking=True)
    project_manager_id = fields.Many2one('project_budget.project_manager', string='project_manager', required=True,
                                         copy=True, default=_get_first_manager_from_access, domain=_get_manager_list, tracking=True)
    customer_organization_id = fields.Many2one('project_budget.customer_organization', string='customer_organization',
                                               required=True, copy=True)
    customer_status_id = fields.Many2one('project_budget.customer_status', string='customer_status', required=True,
                                         copy=True)
    industry_id = fields.Many2one('project_budget.industry', string='industry', required=True, copy=True)
    essence_project = fields.Text(string='essence_project', default = "")
    end_presale_project_quarter = fields.Char(string='End date of the Presale project(quarter)', compute='_compute_quarter', store=True, tracking=True)
    end_presale_project_month = fields.Date(string='Date of transition to the Production Budget(MONTH)', required=True, default=fields.datetime.now(), tracking=True)
    end_sale_project_quarter = fields.Char(string='End date of the Sale project(quarter)', compute='_compute_quarter', store=True, tracking=True)
    end_sale_project_month = fields.Date(string='The period of shipment or provision of services to the Client(MONTH)', required=True,default=fields.datetime.now(), tracking=True)
    vat_attribute_id = fields.Many2one('project_budget.vat_attribute', string='vat_attribute', copy=True, required=True
                                       ,default=lambda self: self.env['project_budget.vat_attribute'].search([], limit=1))
    total_amount_of_revenue = fields.Monetary(string='total_amount_of_revenue', compute='_compute_spec_totals', store=True, tracking=True)
    total_amount_of_revenue_with_vat = fields.Monetary(string='total_amount_of_revenue_with_vat', compute='_compute_spec_totals',
                                              store=True, tracking=True)
    revenue_from_the_sale_of_works =fields.Monetary(string='revenue_from_the_sale_of_works(services)')
    revenue_from_the_sale_of_goods = fields.Monetary(string='revenue_from the sale of goods')
    cost_price = fields.Monetary(string='cost_price', compute='_compute_spec_totals', store=True, tracking=True)
    cost_of_goods = fields.Monetary(string='cost_of_goods')
    own_works_fot = fields.Monetary(string='own_works_fot')
    third_party_works = fields.Monetary(string='third_party_works(subcontracting)')
    awards_on_results_project = fields.Monetary(string='Awards based on the results of the project')
    transportation_expenses = fields.Monetary(string='transportation_expenses')
    travel_expenses = fields.Monetary(string='travel_expenses')
    representation_expenses = fields.Monetary(string='representation_expenses')
    taxes_fot_premiums = fields.Monetary(string='taxes_FOT and premiums', compute='_compute_spec_totals', store=True, tracking=True)
    warranty_service_costs = fields.Monetary(string='Warranty service costs')
    rko_other = fields.Monetary(string='rko_other')
    other_expenses = fields.Monetary(string='other_expenses')
    margin_income = fields.Monetary(string='Margin income', compute='_compute_spec_totals', store=True)
    profitability = fields.Float(string='Profitability(share of Sale margin in revenue)', compute='_compute_spec_totals', store=True, tracking=True)
    estimated_probability_id = fields.Many2one('project_budget.estimated_probability', string='estimated_probability',
                                            default=lambda self: self.env['project_budget.estimated_probability'].search([('name', '=', '30')], limit=1)
                                            , copy = True, tracking=True)
    legal_entity_signing_id = fields.Many2one('project_budget.legal_entity_signing', string='legal_entity_signing a contract from the NCC', required=True, copy=True)
    project_type_id = fields.Many2one('project_budget.project_type',
                                              string='project_type', required=True,
                                              copy=True)
    comments  = fields.Text(string='comments project', default = "")
    technological_direction_id = fields.Many2one('project_budget.technological_direction',
                                              string='technological_direction', required=True,copy=True)
    planned_cash_flow_sum = fields.Monetary(string='planned_cash_flow_sum', compute='_compute_planned_cash_flow_sum',
                                            store=True, tracking=True)
    planned_cash_flow_ids = fields.One2many(
        comodel_name='project_budget.planned_cash_flow',
        inverse_name='projects_id',
        string="planned cash flow", auto_join=True, copy=True)

    step_project_number = fields.Char(string='step project number', store=True, tracking=True)
    dogovor_number = fields.Char(string='Dogovor number', store=True, tracking=True)
    planned_acceptance_flow_sum = fields.Monetary(string='planned_acceptance_flow_sum',
                                                  compute='_compute_planned_acceptance_flow_sum',store=True, tracking=True)
    planned_acceptance_flow_ids = fields.One2many(
        comodel_name='project_budget.planned_acceptance_flow',
        inverse_name='projects_id',
        string="planned acceptance flow", auto_join=True,copy=True)
    fact_cash_flow_sum = fields.Monetary(string='fact_cash_flow_sum', compute='_compute_fact_cash_flow_sum', store=True
                                         , tracking=True)
    fact_cash_flow_ids = fields.One2many(
        comodel_name='project_budget.fact_cash_flow',
        inverse_name='projects_id',
        string="fact cash flow", auto_join=True, copy=True)
    fact_acceptance_flow_sum = fields.Monetary(string='fact_acceptance_flow_sum', compute='_compute_fact_acceptance_flow_sum',
                                               store=True, tracking=True)
    fact_acceptance_flow_ids = fields.One2many(
        comodel_name='project_budget.fact_acceptance_flow',
        inverse_name='projects_id',
        string="fact acceptance flow", auto_join=True,copy=True)

    project_have_steps = fields.Boolean(string="project have steps", default=False, copy=True)
    project_steps_ids = fields.One2many(
        comodel_name='project_budget.project_steps',
        inverse_name='projects_id',
        string="project steps", auto_join=True,copy=True)
    prj_step_sum_without_vat = fields.Monetary(string='project_steps_Sum without_vat', compute='_compute_project_steps_sum',
                                               store=True, tracking=True)
    prj_step_sum_with_vat = fields.Monetary(string='project_steps_Sum with_vat', compute='_compute_project_steps_sum',
                                               store=True, tracking=True)

    @api.depends('estimated_probability_id')
    def _compute_specification_state(self):
        for row in self:
            if row.estimated_probability_id.name == '0':
                row.specification_state = 'cancel'
            if row.estimated_probability_id.name == '30':
                row.specification_state = 'prepare'
            if row.estimated_probability_id.name == '50':
                row.specification_state = 'prepare'
            if row.estimated_probability_id.name == '75':
                row.specification_state = 'prepare'
            if row.estimated_probability_id.name == '100':
                row.specification_state = 'production'

    @api.depends('project_supervisor_id.user_id')
    def _get_supervisor_user_id(self):
        for row in self:
            row.project_supervisor_user_id = row.project_supervisor_id.user_id

    @api.depends('project_manager_id.user_id')
    def _get_manager_user_id(self):
        for row in self:
            row.project_manager_user_id = row.project_manager_id.user_id

    @api.depends("planned_cash_flow_ids.sum_cash")
    def _compute_planned_cash_flow_sum(self):
        for row in self:
            row.planned_cash_flow_sum = 0
            for row_flow in self.planned_cash_flow_ids:
                row.planned_cash_flow_sum = row.planned_cash_flow_sum + row_flow.sum_cash

    @api.depends("project_steps_ids.sum_without_vat")
    def _compute_project_steps_sum(self):
        for row in self:
            row.prj_step_sum_with_vat = 0
            row.prj_step_sum_without_vat = 0
            for row_proj_step in self.project_steps_ids:
                row.prj_step_sum_without_vat = row.prj_step_sum_without_vat + row_proj_step.sum_without_vat
                row.prj_step_sum_with_vat = row.prj_step_sum_with_vat + row_proj_step.sum_with_vat


    @api.depends("planned_acceptance_flow_ids.sum_cash")
    def _compute_planned_acceptance_flow_sum(self):
        for row in self:
            row.planned_acceptance_flow_sum = 0
            for row_flow in self.planned_acceptance_flow_ids:
                row.planned_acceptance_flow_sum = row.planned_acceptance_flow_sum + row_flow.sum_cash

    @api.depends("fact_cash_flow_ids.sum_cash")
    def _compute_fact_cash_flow_sum(self):
        for row in self:
            row.fact_cash_flow_sum = 0
            for row_flow in self.fact_cash_flow_ids:
                row.fact_cash_flow_sum = row.fact_cash_flow_sum + row_flow.sum_cash

    @api.depends("fact_acceptance_flow_ids.sum_cash")
    def _compute_fact_acceptance_flow_sum(self):
        for row in self:
            row.fact_acceptance_flow_sum = 0
            for row_flow in self.fact_acceptance_flow_ids:
                row.fact_acceptance_flow_sum = row.fact_acceptance_flow_sum + row_flow.sum_cash


    @ api.depends("revenue_from_the_sale_of_works", 'revenue_from_the_sale_of_goods', 'cost_of_goods', 'own_works_fot',
    'third_party_works', "awards_on_results_project", 'transportation_expenses', 'travel_expenses', 'representation_expenses',
     "warranty_service_costs", 'rko_other', 'other_expenses','vat_attribute_id','legal_entity_signing_id','project_have_steps',
      'prj_step_sum_with_vat')
    def _compute_spec_totals(self):
        for budget_spec in self:
            budget_spec.total_amount_of_revenue = budget_spec.revenue_from_the_sale_of_works + budget_spec.revenue_from_the_sale_of_goods
            budget_spec.taxes_fot_premiums = (budget_spec.awards_on_results_project + budget_spec.own_works_fot)*budget_spec.legal_entity_signing_id.percent_fot/100
            budget_spec.cost_price = budget_spec.cost_of_goods + budget_spec.own_works_fot+ budget_spec.third_party_works +budget_spec.awards_on_results_project
            budget_spec.cost_price = budget_spec.cost_price + budget_spec.transportation_expenses+budget_spec.travel_expenses+budget_spec.representation_expenses
            budget_spec.cost_price = budget_spec.cost_price + budget_spec.warranty_service_costs+budget_spec.rko_other+budget_spec.other_expenses
            budget_spec.cost_price = budget_spec.cost_price + (budget_spec.awards_on_results_project + budget_spec.own_works_fot) * budget_spec.legal_entity_signing_id.percent_fot / 100
            budget_spec.margin_income = budget_spec.total_amount_of_revenue - budget_spec.cost_price

            if budget_spec.project_have_steps :
                budget_spec.total_amount_of_revenue_with_vat = budget_spec.prj_step_sum_with_vat
            else:
                budget_spec.total_amount_of_revenue_with_vat = (budget_spec.revenue_from_the_sale_of_works + budget_spec.revenue_from_the_sale_of_goods)*(1+budget_spec.vat_attribute_id.percent/100)

            if budget_spec.total_amount_of_revenue == 0 :
                budget_spec.profitability = 0
            else:
                budget_spec.profitability = budget_spec.margin_income / budget_spec.total_amount_of_revenue * 100

    @ api.depends('commercial_budget_id.currency_id','commercial_budget_id.budget_state','commercial_budget_id.currency_id')
    def _compute_reference(self):
        for budget_spec in self:
            budget_spec.currency_id = budget_spec.commercial_budget_id.currency_id
            budget_spec.etalon_budget = budget_spec.commercial_budget_id.etalon_budget
            budget_spec.budget_state = budget_spec.commercial_budget_id.budget_state

    @api.depends('end_presale_project_month','end_sale_project_month')
    def _compute_quarter(self):
        for fieldquarter in self:
            if fieldquarter.end_presale_project_month == False:
                continue
            tmp_date = fieldquarter.end_presale_project_month
            month = tmp_date.month
            year = tmp_date.year
            if 0 <= int(month) <= 3:
                fieldquarter.end_presale_project_quarter = 'Q1 ' + str(year)
            elif 4 <= int(month) <= 6:
                fieldquarter.end_presale_project_quarter = 'Q2 ' + str(year)
            elif 7 <= int(month) <= 9:
                fieldquarter.end_presale_project_quarter = 'Q3 ' + str(year)
            elif 10 <= int(month) <= 12:
                fieldquarter.end_presale_project_quarter = 'Q4 ' + str(year)
            else:
                fieldquarter.end_presale_project_quarter = 'NA'
            tmp_date = fieldquarter.end_sale_project_month
            month = tmp_date.month
            year = tmp_date.year
            if 0 <= int(month) <= 3:
                fieldquarter.end_sale_project_quarter = 'Q1 ' + str(year)
            elif 4 <= int(month) <= 6:
                fieldquarter.end_sale_project_quarter = 'Q2 ' + str(year)
            elif 7 <= int(month) <= 9:
                fieldquarter.end_sale_project_quarter = 'Q3 ' + str(year)
            elif 10 <= int(month) <= 12:
                fieldquarter.end_sale_project_quarter = 'Q4 ' + str(year)
            else:
                fieldquarter.end_sale_project_quarter = 'NA'


    def user_is_supervisor(self,supervisor_id):
        supervisor_access = self.env['project_budget.project_supervisor_access'].search([('user_id.id', '=', self.env.user.id)
                                                                                        ,('project_supervisor_id.id', '=', supervisor_id)
                                                                                        ,('can_approve_project','=',True)])
        if not supervisor_access :
            return False
        else: return True

    def set_approve_manager(self):
        for rows in self:
            # if rows.estimated_probability_id.name in ('50','75','100'):
            #     if rows.total_amount_of_revenue != rows.planned_acceptance_flow_sum:
            #         raisetext = _("DENIED. planned_acceptance_flow_sum <> total_amount_of_revenue")
            #         raise ValidationError(raisetext)
            #
            #     if rows.total_amount_of_revenue_with_vat != rows.planned_cash_flow_sum:
            #         raisetext = _("DENIED. planned_cash_flow_sum <> total_amount_of_revenue_with_vat")
            #         raise ValidationError(raisetext)
            if rows.project_have_steps :
                if rows.total_amount_of_revenue != rows.prj_step_sum_without_vat:
                    raisetext = _("DENIED. \n"+
                                  "Projects have steps, but 'total amount of revenue' <> 'sum step prjoject without vat'")
                    raise ValidationError(raisetext)

            if rows.approve_state=="need_approve_manager" and rows.budget_state == 'work' and rows.specification_state !='cancel':
                rows.write({
                    'approve_state': "need_approve_supervisor"
                })
                    # rows.approve_state="need_approve_supervisor"
        return False

    def set_approve_supervisor(self):
        for rows in self:
            if rows.approve_state=="need_approve_supervisor" and rows.budget_state == 'work' and rows.specification_state !='cancel':
                if self.user_is_supervisor(rows.project_supervisor_id.id) or self.user_has_groups('project_budget.project_budget_admin'):
                    # rows.approve_state="approved"
                   rows.write({
                       'approve_state': "approved"
                     })
        return False

    def cancel_approve(self):
        for rows in self:
            if (rows.approve_state=="approved" or rows.approve_state=="need_approve_supervisor") and rows.budget_state == 'work' and rows.specification_state !='cancel':
                if self.user_is_supervisor(rows.project_supervisor_id.id) or self.user_has_groups('project_budget.project_budget_admin'):
                    # rows.approve_state="need_approve_manager"
                    rows.write({
                        'approve_state': "need_approve_manager"
                    })
        return False

    def open_record(self):
        self.ensure_one()
        # first you need to get the id of your record
        # you didn't specify what you want to edit exactly
        rec_id = self.id
        # then if you have more than one form view then specify the form id
        form_id = self.env.ref('project_budget.show_comercial_budget_spec_form')
        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Project',
            'res_model': 'project_budget.projects',
            'res_id': rec_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            # if you want to open the form in edit mode direclty
            'flags': {'initial_mode': 'edit'},
            'target': 'new',
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('project_id') or vals['project_id'] == 'ID':
                vals['project_id'] = self.env['ir.sequence'].sudo().next_by_code('project_budget.projects')
        return super().create(vals_list)

    def unlink(self):
        """ dont delete.
        Set specification_state to 'cancel'
        """
        for record in self:
            if record.approve_state == 'need_approve_manager' :
                record.write({
                            'specification_state': "cancel"
                        })
            else:
                raisetext = _("only in state 'need approve manager' project can be canceled")
                raise ValidationError(raisetext)

        return False