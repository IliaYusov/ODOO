from psycopg2 import sql

from odoo import fields, models, tools


class TimesheetReportAnalysis(models.Model):
    _name = 'hr.timesheet.report.analysis'
    _description = 'Timesheet Report Analysis'
    _auto = False

    name = fields.Char(string='Description', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True)
    milestone_id = fields.Many2one('task.task', string='Milestone', readonly=True)
    task_id = fields.Many2one('task.task', string='Task', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    amount = fields.Monetary(string='Amount', readonly=True)
    unit_amount = fields.Float(string='Hours Spent', readonly=True)

    def _select(self):
        return """
            a.id AS id,
            a.name AS name,
            a.user_id AS user_id,
            a.project_id AS project_id,
            a.milestone_id AS milestone_id,            
            a.task_id AS task_id,
            a.employee_id AS employee_id,
            a.manager_id AS manager_id,
            a.company_id AS company_id,
            a.department_id AS department_id,
            a.currency_id AS currency_id,
            a.date AS date,
            a.amount AS amount,
            a.unit_amount AS unit_amount
        """

    def _from(self):
        return """
            account_analytic_line a
        """

    def _where(self):
        return """
            a.project_id IS NOT NULL
        """

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """            
            SELECT %s
            FROM %s
            WHERE %s
        """ % (self._select(), self._from(), self._where())
        self.env.cr.execute(
            sql.SQL("CREATE or REPLACE VIEW {} as ({})").format(
                sql.Identifier(self._table),
                sql.SQL(query)
            )
        )
