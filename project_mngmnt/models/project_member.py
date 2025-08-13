from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectMember(models.Model):
    _name = 'project.member'
    _description = 'Project Member'
    _order = 'id'

    project_id = fields.Many2one('project.project', string='Project', index=True, ondelete='cascade')
    company_id = fields.Many2one(related='project_id.company_id', string='Company', readonly=True)
    can_edit = fields.Boolean(related='project_id.can_edit', readonly=True)
    role_id = fields.Many2one('project.role', string='Project Role', ondelete='restrict', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                  required=True)
    date_start = fields.Date(string='Start Date', default=fields.Date.today, required=True)
    date_end = fields.Date(string='End Date', required=True)

    _sql_constraints = [
        ('project_participation_date_end_greater', 'check(date_end >= date_start)', 'The participation in the project start date must be before its end date.')
    ]

    # ------------------------------------------------------
    # CONSTRAINS
    # ------------------------------------------------------

    @api.constrains('employee_id', 'role_id', 'date_start', 'date_end')
    def _must_not_have_overlapping_roles(self):
        for rec in self:
            for member in rec.project_id.project_member_ids:
                if member != rec and member.employee_id == rec.employee_id and member.role_id == rec.role_id and member.date_start <= rec.date_end and member.date_end >= rec.date_start:
                    raise ValidationError(_("Overlapping roles."))
