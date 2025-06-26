from odoo import fields, models


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
