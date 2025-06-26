from psycopg2 import sql

from odoo import tools
from odoo import fields, models


class CrmHoldingCustomerReport(models.Model):
    _name = 'crm.holding.customer.report'
    _description = 'Holding Customer Report'
    _auto = False

    customer_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    industry_id = fields.Many2one('res.partner.industry', string='Industry', readonly=True)
    technological_direction_id = fields.Many2one('project_budget.technological_direction',
                                                 string='Technological Direction', readonly=True)
    key_account_manager_id = fields.Many2one('hr.employee', string='Key Account Manager', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    def _select(self):
        return """
            row_number() OVER () as id,
            l.partner_id as customer_id,            
            l.industry_id,
            l.technological_direction_id,
            l.key_account_manager_id,
            usr.company_id                            
        """

    def _from(self):
        return """
            project_budget_projects l
        """

    def _join(self):
        return """
            INNER JOIN project_budget_project_stage ps ON ps.id = l.stage_id AND ps.project_state <> 'cancel'             
            INNER JOIN account_analytic_account a ON a.id = l.responsibility_center_id AND a.name <> 'Корректировка ФЭД'
            INNER JOIN hr_employee emp ON emp.id = l.key_account_manager_id
            INNER JOIN res_users usr ON usr.id = emp.user_id            
        """

    def _where(self):
        return """
            l.step_status = 'project' AND l.budget_state = 'work' AND l.active = true
        """

    def _group_by(self):
        return """
            l.partner_id,
            l.industry_id,
            l.technological_direction_id,
            l.key_account_manager_id,
            usr.company_id            
        """

    def init(self):
        query = """            
            SELECT %s
            FROM %s
            %s
            WHERE %s
            GROUP BY %s
        """ % (self._select(), self._from(), self._join(), self._where(), self._group_by())
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table),
                sql.SQL(query)
            ))
