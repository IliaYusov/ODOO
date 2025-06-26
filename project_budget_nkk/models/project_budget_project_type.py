from odoo import models, fields


class ProjectType(models.Model):
    _name = 'project_budget.project_type'
    _description = 'Project Type'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    descr = fields.Char(string='Description', translate=True)
