from odoo import fields, models


class TaskReportAnalysis(models.Model):
    _inherit = 'task.task.report.analysis'

    project_id = fields.Many2one('project.project', string='Project', readonly=True,
                                 groups='project_mngmnt.project_group_user')
    planned_hours = fields.Float(string='Planned Hours', readonly=True,
                                 groups='hr_timesheet_mngmnt.hr_timesheet_group_user')
    effective_hours = fields.Float(string='Hours Spent', readonly=True,
                                   groups='hr_timesheet_mngmnt.hr_timesheet_group_user')

    def _select(self):
        return super()._select() + """,
            project_id,
            COALESCE(t.planned_hours, 0) as planned_hours,
            t.effective_hours
        """

    def _where(self):
        return """
            t.project_id IS NOT NULL
        """

    def _group_by(self):
        return super()._group_by() + """,
            project_id,
            t.planned_hours,
            t.effective_hours
        """
