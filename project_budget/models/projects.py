from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import pytz
from datetime import timedelta

class projects(models.Model):
    _name = 'project_budget.projects'
    _description = "project_office commercial budget projects"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_to_show'
    _check_company_auto = True
    # _rec_names_search = ['project_id', 'essence_project']

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

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    project_id = fields.Char(string="Project_ID", required=True, index=True, copy=True, group_operator = 'count',
                             default='ID') #lambda self: self.env['ir.sequence'].sudo().next_by_code('project_budget.projects'))
    specification_state = fields.Selection([('prepare', 'Prepare'), ('production', 'Production'), ('cancel','Canceled')], required=True,
                                           index=True, default='prepare', store=True, copy=True, tracking=True, compute="_compute_specification_state")
    approve_state= fields.Selection([('need_approve_manager', 'need managers approve'), ('need_approve_supervisor', 'need supervisors approve'), ('approved','approved')],
                                    required=True, index=True, default='need_approve_manager', store=True, copy=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Account Currency',  required = True, copy = True,
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'RUB')], limit=1),tracking=True)
    etalon_budget = fields.Boolean(related='commercial_budget_id.etalon_budget', readonly=True)
    date_actual = fields.Datetime(related='commercial_budget_id.date_actual', readonly=True, store=True)
    isRukovoditel_required_in_project = fields.Boolean(related='project_office_id.isRukovoditel_required_in_project', readonly=True, store=True)
    commercial_budget_id = fields.Many2one('project_budget.commercial_budget', string='commercial_budget-',required=True, ondelete='cascade', index=True, copy=False
                                           ,default=lambda self: self.env['project_budget.commercial_budget'].search([('budget_state', '=', 'work')], limit=1)
                                           , domain=_get_commercial_budget_list)
    was_changes = fields.Boolean(string="was_changes", copy=True, default = True)
    vgo = fields.Selection([('-', '-'), ('vgo1', 'vgo1'),('vgo2', 'vgo2')], required=True, default='-', copy = True,tracking=True)

    # budget_state = fields.Selection([('work', 'Working'), ('fixed', 'Fixed')], required=True, index=True, default='work', copy = False,
    #                                 compute='_compute_reference', store=True, tracking=True)

    budget_state = fields.Selection(related = 'commercial_budget_id.budget_state', readonly = True, index=True, store=True)

    project_office_id = fields.Many2one('project_budget.project_office', string='project_office', required=True,
                                        copy=True,tracking=True)
    project_supervisor_id = fields.Many2one('project_budget.project_supervisor', string='project_supervisor',
                                            required=True, copy=True, domain=_get_supervisor_list, tracking=True)
    project_manager_id = fields.Many2one('project_budget.project_manager', string='project_manager', required=True,
                                         copy=True, default=_get_first_manager_from_access, domain=_get_manager_list, tracking=True) # на самом деле это КАМ, а вот РП ниже

    rukovoditel_project_id = fields.Many2one('project_budget.rukovoditel_project', string='rukovoditel_project',
                                         copy=True,  tracking=True)

    customer_organization_id = fields.Many2one('project_budget.customer_organization', string='customer_organization',
                                               required=True, copy=True,tracking=True)
    customer_status_id = fields.Many2one('project_budget.customer_status', string='customer_status', required=True,
                                         copy=True,tracking=True)
    industry_id = fields.Many2one('project_budget.industry', string='industry', required=True, copy=True,tracking=True)
    essence_project = fields.Text(string='essence_project', default = "",tracking=True)
    end_presale_project_quarter = fields.Char(string='End date of the Presale project(quarter)', compute='_compute_quarter', store=True, tracking=True)
    end_presale_project_month = fields.Date(string='Date of transition to the Production Budget(MONTH)', required=True, default=fields.datetime.now(), tracking=True)
    end_sale_project_quarter = fields.Char(string='End date of the Sale project(quarter)', compute='_compute_quarter', store=True, tracking=True)
    end_sale_project_month = fields.Date(string='The period of shipment or provision of services to the Client(MONTH)', required=True,default=fields.datetime.now(), tracking=True)
    vat_attribute_id = fields.Many2one('project_budget.vat_attribute', string='vat_attribute', copy=True,tracking=True)
                                       # default=lambda self: self.env['project_budget.vat_attribute'].search([], limit=1))
    total_amount_of_revenue = fields.Monetary(string='total_amount_of_revenue', compute='_compute_spec_totals', store=True, tracking=True)
    total_amount_of_revenue_with_vat = fields.Monetary(string='total_amount_of_revenue_with_vat', compute='_compute_spec_totals',
                                              store=True, tracking=True)
    revenue_from_the_sale_of_works =fields.Monetary(string='revenue_from_the_sale_of_works(services)',tracking=True)
    revenue_from_the_sale_of_goods = fields.Monetary(string='revenue_from the sale of goods',tracking=True)
    cost_price = fields.Monetary(string='cost_price', compute='_compute_spec_totals', store=True, tracking=True)
    cost_of_goods = fields.Monetary(string='cost_of_goods',tracking=True)
    own_works_fot = fields.Monetary(string='own_works_fot',tracking=True)
    third_party_works = fields.Monetary(string='third_party_works(subcontracting)',tracking=True)
    awards_on_results_project = fields.Monetary(string='Awards based on the results of the project',tracking=True)
    transportation_expenses = fields.Monetary(string='transportation_expenses',tracking=True)
    travel_expenses = fields.Monetary(string='travel_expenses',tracking=True)
    representation_expenses = fields.Monetary(string='representation_expenses',tracking=True)
    taxes_fot_premiums = fields.Monetary(string='taxes_FOT and premiums', compute='_compute_spec_totals', store=True, tracking=True)
    warranty_service_costs = fields.Monetary(string='Warranty service costs',tracking=True)
    rko_other = fields.Monetary(string='rko_other',tracking=True)
    other_expenses = fields.Monetary(string='other_expenses',tracking=True)
    margin_income = fields.Monetary(string='Margin income', compute='_compute_spec_totals', store=True)
    profitability = fields.Float(string='Profitability(share of Sale margin in revenue)', compute='_compute_spec_totals', store=True, tracking=True)
    estimated_probability_id = fields.Many2one('project_budget.estimated_probability', string='estimated_probability',  copy = True, tracking=True,required = True,
                help = "*The estimated probability of project implementation is selected from the following categories:"
                       "\n"
                       "\n30% The Customer's need for supply/services has been identified, the technical and commercial feasibility of their implementation has been determined, financing mechanisms are available/identified."
                       "\n Financing mechanisms are being/identified. Proactive creation of a new need for the Customer by the efforts of the seller, for which the Customer will organize or provide subsequent financing of the project."
                       "\n"
                       "\n50% of the Customer's requirements, financing and procurement deadlines are determined in a specific financial period, there is a TAP from the Vendor / Supplier, there is Customer support"
                       "\n at the same time, it is necessary to finalize the terms of interaction according to the project, both with the Vendor / Supplier and with the Customer, there is a clear understanding of how to do this."
                       "\n financing of the presale is allowed only after the creation of the presale"
                       "\n 75% Meets the formed requirements of the CD/ TOR for the implementation of the project, protection from the Vendor / Supplier has been received,"
                       "\n the project budget has been approved by the Director of the Software or CD, the timing of procurement procedures from the Customer does not interfere with the implementation of the project."
                       "\n"
                       "\n 100% The project has moved to the production budget."
            )
                                            # ,default=lambda self: self.env['project_budget.estimated_probability'].search([('name', '=', '30')], limit=1)

    legal_entity_signing_id = fields.Many2one('project_budget.legal_entity_signing', string='legal_entity_signing a contract from the NCC', required=True, copy=True,tracking=True)
    project_type_id = fields.Many2one('project_budget.project_type',string='project_type', required=True,copy=True,tracking=True)

    is_revenue_from_the_sale_of_works =fields.Boolean(related='project_type_id.is_revenue_from_the_sale_of_works', readonly=True)
    is_revenue_from_the_sale_of_goods = fields.Boolean(related='project_type_id.is_revenue_from_the_sale_of_goods', readonly=True)
    is_cost_of_goods = fields.Boolean(related='project_type_id.is_cost_of_goods', readonly=True)
    is_own_works_fot = fields.Boolean(related='project_type_id.is_own_works_fot', readonly=True)
    is_third_party_works = fields.Boolean(related='project_type_id.is_third_party_works', readonly=True)
    is_awards_on_results_project = fields.Boolean(related='project_type_id.is_awards_on_results_project', readonly=True)
    is_transportation_expenses = fields.Boolean(related='project_type_id.is_transportation_expenses', readonly=True)
    is_travel_expenses = fields.Boolean(related='project_type_id.is_travel_expenses', readonly=True)
    is_representation_expenses = fields.Boolean(related='project_type_id.is_representation_expenses', readonly=True)
    is_warranty_service_costs = fields.Boolean(related='project_type_id.is_warranty_service_costs', readonly=True)
    is_rko_other = fields.Boolean(related='project_type_id.is_rko_other', readonly=True)
    is_other_expenses = fields.Boolean(related='project_type_id.is_other_expenses', readonly=True)

    comments  = fields.Text(string='comments project', default = "")
    technological_direction_id = fields.Many2one('project_budget.technological_direction',
                                              string='technological_direction', required=True,copy=True,tracking=True)
    planned_cash_flow_sum = fields.Monetary(string='planned_cash_flow_sum', compute='_compute_planned_cash_flow_sum',
                                            store=False, tracking=True)
    planned_cash_flow_ids = fields.One2many(
        comodel_name='project_budget.planned_cash_flow',
        inverse_name='projects_id',
        string="planned cash flow", auto_join=True, copy=True)

    step_project_number = fields.Char(string='step project number', store=True, tracking=True)
    dogovor_number = fields.Char(string='Dogovor number', store=True, tracking=True)
    planned_acceptance_flow_sum = fields.Monetary(string='planned_acceptance_flow_sum',
                                                  compute='_compute_planned_acceptance_flow_sum',store=False, tracking=True)
    planned_acceptance_flow_ids = fields.One2many(
        comodel_name='project_budget.planned_acceptance_flow',
        inverse_name='projects_id',
        string="planned acceptance flow", auto_join=True,copy=True)
    fact_cash_flow_sum = fields.Monetary(string='fact_cash_flow_sum', compute='_compute_fact_cash_flow_sum', store=False
                                         , tracking=True)
    fact_cash_flow_ids = fields.One2many(
        comodel_name='project_budget.fact_cash_flow',
        inverse_name='projects_id',
        string="fact cash flow", auto_join=True, copy=True)
    fact_acceptance_flow_sum = fields.Monetary(string='fact_acceptance_flow_sum', compute='_compute_fact_acceptance_flow_sum',
                                               store=False, tracking=True)
    fact_acceptance_flow_ids = fields.One2many(
        comodel_name='project_budget.fact_acceptance_flow',
        inverse_name='projects_id',
        string="fact acceptance flow", auto_join=True,copy=True)

    project_have_steps = fields.Boolean(string="project have steps", default=False, copy=True,tracking=True)
    is_framework = fields.Boolean(string="project is framework", default=False, copy=True,tracking=True)
    project_steps_ids = fields.One2many(
        comodel_name='project_budget.project_steps',
        inverse_name='projects_id',
        string="project steps", auto_join=True,copy=True)

    name_to_show = fields.Char(string='name_to_show', compute='_get_name_to_show')

    @api.depends('project_id','step_project_number')
    def _get_name_to_show(self):
        for prj in self:
            prj.name_to_show = prj.project_id + '|'+ (prj.step_project_number or '') + '|' + (prj.essence_project[:30] or '')+'...'

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


    @api.onchange('project_office_id','specification_state','currency_id','project_supervisor_id','project_manager_id',
                  'customer_status_id','industry_id','essence_project','end_presale_project_month','end_sale_project_month','vat_attribute_id','total_amount_of_revenue',
                  'total_amount_of_revenue_with_vat','revenue_from_the_sale_of_works','revenue_from_the_sale_of_goods','cost_price','cost_of_goods','own_works_fot',
                  'third_party_works','awards_on_results_project','transportation_expenses','travel_expenses','representation_expenses','taxes_fot_premiums','warranty_service_costs',
                  'rko_other','other_expenses','margin_income','profitability','estimated_probability_id','legal_entity_signing_id','project_type_id','comments','technological_direction_id',
                  'planned_cash_flow_sum','planned_cash_flow_ids','step_project_number','dogovor_number','planned_acceptance_flow_sum','planned_acceptance_flow_ids','fact_cash_flow_sum',
                  'fact_cash_flow_ids','fact_acceptance_flow_sum','fact_acceptance_flow_ids','project_have_steps','project_steps_ids'
                )
    def _check_changes_project(self):
        print('_check_changes_project')
        for row in self:
            print('row.was_changes = ', row.id)
            if row.was_changes == False:
                try:
                    cur_idstr = str(row.id)
                    cur_idstr = cur_idstr.replace('NewId_','')
                    cur_id = int(cur_idstr)
                    curprj = self.env['project_budget.projects'].search([('id', '=', cur_id)],limit=1)
                    print(cur_id)
                    if curprj:
                        curprj.was_changes = True
                except: return False
            if row.project_have_steps == False:
                if row.project_type_id.is_revenue_from_the_sale_of_works == False: row.revenue_from_the_sale_of_works = 0
                if row.project_type_id.is_revenue_from_the_sale_of_goods == False: row.revenue_from_the_sale_of_goods = 0
                if row.project_type_id.is_cost_of_goods == False: row.cost_of_goods = 0
                if row.project_type_id.is_own_works_fot == False: row.own_works_fot = 0
                if row.project_type_id.is_third_party_works == False: row.third_party_works = 0
                if row.project_type_id.is_awards_on_results_project == False: row.awards_on_results_project = 0
                if row.project_type_id.is_transportation_expenses == False: row.transportation_expenses = 0
                if row.project_type_id.is_travel_expenses== False: row.travel_expenses = 0
                if row.project_type_id.is_representation_expenses== False: row.representation_expenses = 0
                if row.project_type_id.is_warranty_service_costs == False: row.warranty_service_costs = 0
                if row.project_type_id.is_rko_other == False: row.rko_other = 0
                if row.project_type_id.is_other_expenses== False: row.other_expenses = 0


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
            for row_flow in row.planned_cash_flow_ids:
                row.planned_cash_flow_sum = row.planned_cash_flow_sum + row_flow.sum_cash


    @api.depends("planned_acceptance_flow_ids.sum_cash")
    def _compute_planned_acceptance_flow_sum(self):
        for row in self:
            row.planned_acceptance_flow_sum = 0
            for row_flow in row.planned_acceptance_flow_ids:
                row.planned_acceptance_flow_sum = row.planned_acceptance_flow_sum + row_flow.sum_cash

    @api.depends("fact_cash_flow_ids.sum_cash")
    def _compute_fact_cash_flow_sum(self):
        for row in self:
            row.fact_cash_flow_sum = 0
            for row_flow in row.fact_cash_flow_ids:
                row.fact_cash_flow_sum = row.fact_cash_flow_sum + row_flow.sum_cash

    @api.depends("fact_acceptance_flow_ids.sum_cash")
    def _compute_fact_acceptance_flow_sum(self):
        for row in self:
            row.fact_acceptance_flow_sum = 0
            for row_flow in row.fact_acceptance_flow_ids:
                row.fact_acceptance_flow_sum = row.fact_acceptance_flow_sum + row_flow.sum_cash

    @api.depends("project_steps_ids.revenue_from_the_sale_of_works", 'project_steps_ids.revenue_from_the_sale_of_goods', 'project_steps_ids.cost_of_goods', 'project_steps_ids.own_works_fot',
                 'project_steps_ids.third_party_works', "project_steps_ids.awards_on_results_project", 'project_steps_ids.transportation_expenses', 'project_steps_ids.travel_expenses',
                 'project_steps_ids.representation_expenses',"project_steps_ids.warranty_service_costs", 'project_steps_ids.rko_other', 'project_steps_ids.other_expenses',
                 'project_steps_ids.vat_attribute_id'
                 ,"revenue_from_the_sale_of_works", 'revenue_from_the_sale_of_goods', 'cost_of_goods', 'own_works_fot',
                 'third_party_works', "awards_on_results_project", 'transportation_expenses', 'travel_expenses', 'representation_expenses',
                 "warranty_service_costs", 'rko_other', 'other_expenses','vat_attribute_id','legal_entity_signing_id','project_have_steps',)
    def _compute_spec_totals(self):
        for budget_spec in self:
            if budget_spec.project_have_steps == False :
                budget_spec.total_amount_of_revenue = budget_spec.revenue_from_the_sale_of_works + budget_spec.revenue_from_the_sale_of_goods
                budget_spec.taxes_fot_premiums = (budget_spec.awards_on_results_project + budget_spec.own_works_fot)*budget_spec.legal_entity_signing_id.percent_fot/100
                budget_spec.cost_price = budget_spec.cost_of_goods + budget_spec.own_works_fot+ budget_spec.third_party_works +budget_spec.awards_on_results_project
                budget_spec.cost_price = budget_spec.cost_price + budget_spec.transportation_expenses+budget_spec.travel_expenses+budget_spec.representation_expenses
                budget_spec.cost_price = budget_spec.cost_price + budget_spec.warranty_service_costs+budget_spec.rko_other+budget_spec.other_expenses
                budget_spec.cost_price = budget_spec.cost_price + (budget_spec.awards_on_results_project + budget_spec.own_works_fot) * budget_spec.legal_entity_signing_id.percent_fot / 100
                budget_spec.margin_income = budget_spec.total_amount_of_revenue - budget_spec.cost_price
                budget_spec.total_amount_of_revenue_with_vat = (budget_spec.revenue_from_the_sale_of_works + budget_spec.revenue_from_the_sale_of_goods)*(1+budget_spec.vat_attribute_id.percent/100)
            else:
                budget_spec.total_amount_of_revenue = 0
                budget_spec.cost_price = 0
                budget_spec.margin_income = 0
                budget_spec.total_amount_of_revenue_with_vat = 0
                budget_spec.taxes_fot_premiums = 0
                budget_spec.profitability = 0
                budget_spec.revenue_from_the_sale_of_works = 0
                budget_spec.revenue_from_the_sale_of_goods = 0
                budget_spec.cost_of_goods = 0
                budget_spec.own_works_fot = 0
                budget_spec.third_party_works = 0
                budget_spec.awards_on_results_project = 0
                budget_spec.transportation_expenses = 0
                budget_spec.travel_expenses = 0
                budget_spec.representation_expenses = 0
                budget_spec.warranty_service_costs = 0
                budget_spec.rko_other = 0
                budget_spec.other_expenses = 0
                for step in budget_spec.project_steps_ids:
                    budget_spec.total_amount_of_revenue += step.total_amount_of_revenue
                    budget_spec.cost_price += step.cost_price
                    budget_spec.margin_income += step.margin_income
                    budget_spec.total_amount_of_revenue_with_vat += step.total_amount_of_revenue_with_vat
                    budget_spec.taxes_fot_premiums += step.taxes_fot_premiums
                    budget_spec.revenue_from_the_sale_of_works += step.revenue_from_the_sale_of_works
                    budget_spec.revenue_from_the_sale_of_goods += step.revenue_from_the_sale_of_goods
                    budget_spec.cost_of_goods += step.cost_of_goods
                    budget_spec.own_works_fot += step.own_works_fot
                    budget_spec.third_party_works += step.third_party_works
                    budget_spec.awards_on_results_project += step.awards_on_results_project
                    budget_spec.transportation_expenses += step.transportation_expenses
                    budget_spec.travel_expenses += step.travel_expenses
                    budget_spec.representation_expenses += step.representation_expenses
                    budget_spec.warranty_service_costs += step.warranty_service_costs
                    budget_spec.rko_other += step.rko_other
                    budget_spec.other_expenses += step.other_expenses

            if budget_spec.total_amount_of_revenue == 0:
                budget_spec.profitability = 0
            else:
                budget_spec.profitability = budget_spec.margin_income / budget_spec.total_amount_of_revenue * 100



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



    def print_budget(self):
        for rows in self:
            print()

    def set_approve_manager(self):
        for rows in self:
            # if rows.estimated_probability_id.name in ('50','75','100'):
            #     if rows.total_amount_of_revenue_with_vat != rows.planned_acceptance_flow_sum:
            #         raisetext = _("DENIED. planned_acceptance_flow_sum <> total_amount_of_revenue_with_vat")
            #         raise ValidationError(raisetext)
            #
            #     if rows.total_amount_of_revenue_with_vat != rows.planned_cash_flow_sum:
            #         raisetext = _("DENIED. planned_cash_flow_sum <> total_amount_of_revenue_with_vat")
            #         raise ValidationError(raisetext)

            if rows.approve_state=="need_approve_manager" and rows.budget_state == 'work' and rows.specification_state !='cancel':
                rows.write({
                    'approve_state': "need_approve_supervisor"
                })
                print('rows.id = ', rows.id)

                # Get a reference to the mail.activity model
                activity_model = self.env['mail.activity']
                # Use the search method to find the activities that need to be marked as done
                activities = activity_model.search([('res_id','=', rows.id),
                                                    ('activity_type_id','=',self.env.ref('project_budget.mail_act_send_project_to_supervisor_for_approval').id)
                                                   ])
                print('activities = ', activities)
                # Update the state of each activity to 'done'
                for activitie in activities:
                    activitie.action_done()

                user_id = rows.project_supervisor_id.user_id.id
                print('user_id = ',user_id)
                if rows.project_office_id.receive_tasks_for_approve_project: # не куратору посылать, а руководителю проектного офиса надо
                    if rows.project_office_id.user_id: # вдруг просто галочка стоит, а пользователь не выбран
                        user_id = rows.project_office_id.user_id.id
                print('user_id (after project_office_id) = ', user_id)
                res_model_id_project_budget = self.env['ir.model'].search([('model', '=', 'project_budget.projects')]).id
                print('res_model_id_project_budget = ', res_model_id_project_budget)
                self.env['mail.activity'].create({
                    'display_name': _('You have to approve or decline project'),
                    'summary': _('You have to approve or decline project'),
                    'date_deadline': fields.datetime.now(),
                    'user_id': user_id,
                    'res_id': rows.id,
                    'res_model_id': res_model_id_project_budget,
                    'activity_type_id': self.env.ref('project_budget.mail_act_approve_project_by_supervisor').id
                    })

                    # rows.approve_state="need_approve_supervisor"
        return False

    def set_approve_supervisor(self):
        for rows in self:
            if rows.approve_state=="need_approve_supervisor" and rows.budget_state == 'work' and rows.specification_state !='cancel':

                user_id = False
                if rows.project_office_id.receive_tasks_for_approve_project: # не только куратор может утвекрждать, но и руководитель проектного офиса надо
                    if rows.project_office_id.user_id: # вдруг просто галочка стоит, а пользователь не выбран
                        user_id = rows.project_office_id.user_id.id

                if self.user_is_supervisor(rows.project_supervisor_id.id) or self.user_has_groups('project_budget.project_budget_admin') or self.env.user.id == user_id :
                    # rows.approve_state="approved"
                   rows.write({
                       'approve_state': "approved"
                     })
                   activity_model = self.env['mail.activity']
                   activities = activity_model.search([('res_id', '=', rows.id),
                                                        ('activity_type_id', '=', self.env.ref(
                                                            'project_budget.mail_act_approve_project_by_supervisor').id)
                                                        ])
                   # Update the state of each activity to 'done'
                   for activitie in activities:
                       activitie.action_done()
        return False

    def cancel_approve(self):
        for rows in self:
            if (rows.approve_state=="approved" or rows.approve_state=="need_approve_supervisor") and rows.budget_state == 'work' and rows.specification_state !='cancel':
                user_id = False
                if rows.project_office_id.receive_tasks_for_approve_project: # не только куратор может утвекрждать, но и руководитель проектного офиса надо
                    if rows.project_office_id.user_id: # вдруг просто галочка стоит, а пользователь не выбран
                        user_id = rows.project_office_id.user_id.id

                if self.user_is_supervisor(rows.project_supervisor_id.id) or self.user_has_groups('project_budget.project_budget_admin') or self.env.user.id == user_id :
                    # rows.approve_state="need_approve_manager"
                    rows.write({
                        'approve_state': "need_approve_manager"
                    })
                    activity_model = self.env['mail.activity']
                    activities = activity_model.search([('res_id','=', rows.id),
                                                        ('activity_type_id','=',self.env.ref('project_budget.mail_act_approve_project_by_supervisor').id)
                                                       ])
                    # Update the state of each activity to 'done'
                    for activitie in activities:
                        activitie.action_done()

                    self.env['mail.activity'].create({
                        'display_name': _('Supervisor declined project. Change nessesary values and send supervisor for approval'),
                        'summary': _('Supervisor declined project. Change nessesary values and send supervisor for approval'),
                        'date_deadline': fields.datetime.now(),
                        'user_id': rows.project_manager_id.user_id.id,
                        'res_id': rows.id,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'project_budget.projects')]).id,
                        'activity_type_id': self.env.ref('project_budget.mail_act_send_project_to_supervisor_for_approval').id
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