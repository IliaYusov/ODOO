from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = 'task.task'

    planned_date_begin = fields.Datetime(string='Planned Start Date', tracking=True)
    project_id = fields.Many2one('project.project', string='Project', compute='_compute_project_id',
                                 groups='project_mngmnt.project_group_user', store=True)

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('planned_date_begin', 'date_deadline')
    def _check_date_range(self):
        for rec in self.filtered(lambda t: t.project_id):
            if not rec.project_id.date_start <= fields.Date.to_date(rec.planned_date_begin) <= rec.project_id.date_end \
                    or not rec.project_id.date_start <= fields.Date.to_date(rec.date_deadline) <= rec.project_id.date_end:
                raise ValidationError(_("Planned dates of task should be in project's dates."))

    @api.constrains('planned_hours')
    def _check_planned_hours(self):
        for rec in self.filtered(lambda t: t.project_id and t.parent_id):
            if rec.parent_id.planned_hours < rec.parent_id.subtask_planned_hours:
                raise ValidationError(_("Sum planned hours of subtask's must not exceed planned hours of parent task."))

    @api.constrains('parent_ref_type', 'root_task_id')
    def _check_only_manager_create_milestone(self):
        for task in self:
            if not self.user_has_groups('project_mngmnt.project_group_project_manager, project_mngmnt.project_group_manager') and task.parent_ref_type == 'project.project' and not task.root_task_id:
                raise ValidationError(_('Only Project Manager could create a Milestone.'))

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('parent_ref_type', 'parent_ref_id')
    def _compute_project_id(self):
        for rec in self:
            rec.project_id = rec.parent_ref_id if rec.parent_ref_type == 'project.project' else False

    @api.depends('company_id', 'project_id')
    def _compute_user_ids_domain(self):
        super(Task, self)._compute_user_ids_domain()
        for rec in self:
            if rec.parent_ref_type == 'project.project':
                if not rec.date_deadline:
                    project_members = rec.project_id.project_member_ids.mapped('employee_id.user_id')
                else:
                    project_members = rec.project_id.project_member_ids.filtered(
                        lambda m: m.date_start <= fields.Date.to_date(rec.date_deadline) <= m.date_end).mapped(
                        'employee_id.user_id')
                rec.user_ids_domain += [
                    ('id', 'in', project_members.ids)
                ]
