from psycopg2 import sql

from odoo import api, fields, models, tools
from ..models.task_task import PRIORITIES


class TaskReportAnalysis(models.Model):
    _name = 'task.task.report.analysis'
    _description = 'Tasks Analysis Report'
    _order = 'name desc'
    _auto = False

    @api.model
    def _selection_parent_model(self):
        return [(model.model, model.name) for model in self.env['ir.model'].sudo().search([])]

    task_id = fields.Many2one('task.task', string='Task', readonly=True)
    create_date = fields.Datetime(string='Create Date', readonly=True)
    parent_ref = fields.Reference(selection='_selection_parent_model', string='Parent', readonly=True)
    parent_ref_id = fields.Integer(readonly=True)
    parent_ref_type = fields.Char(readonly=True)
    user_ids = fields.Many2many('res.users', relation='task_user_rel', column1='task_id', column2='user_id',
                                string='Assignees', readonly=True)
    date_deadline = fields.Datetime(string='Deadline', readonly=True)
    date_closed = fields.Datetime(string='Date Closed', readonly=True)
    parent_id = fields.Many2one('task.task', string='Parent Task', readonly=True)
    type_id = fields.Many2one('task.type', string='Task Type', readonly=True)
    stage_id = fields.Many2one('task.stage_id', string='Stage', readonly=True)
    priority = fields.Selection(selection=PRIORITIES, string='Priority', readonly=True)
    is_closed = fields.Boolean(string='Is Closed', readonly=True)
    company_ids = fields.Many2one('res.company', relation='res_company_task_task_rel', column1='task_task_id',
                                  column2='res_company_id', string='Companies', readonly=True)
    active = fields.Boolean(readonly=True)
    description = fields.Text(readonly=True)

    def _select(self):
        return """
            t.id as id,
            t.id as task_id,            
            t.create_date,
            t.parent_ref,
            t.parent_ref_id,
            t.parent_ref_type,            
            t.date_deadline,
            t.date_closed,                        
            t.parent_id,
            t.type_id,
            t.stage_id,
            t.priority,
            t.is_closed,
            t.active,
            t.description                
        """

    def _group_by(self):
        return """
            t.id,
            t.id,            
            t.create_date,
            t.parent_ref,
            t.parent_ref_id,
            t.parent_ref_type,            
            t.date_deadline,
            t.date_closed,                        
            t.parent_id,
            t.type_id,
            t.stage_id,
            t.priority,
            t.is_closed,
            t.active,
            t.description
        """

    def _from(self):
        return """
            task_task t
        """

    def _where(self):
        return """
            t.parent_ref IS NOT NULL
        """

    def init(self):
        query = """            
            SELECT %s
            FROM %s
            WHERE %s
            GROUP BY %s
        """ % (self._select(), self._from(), self._where(), self._group_by())
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("""CREATE or REPLACE VIEW {} as ({})""").format(
                sql.Identifier(self._table),
                sql.SQL(query)
            ))
