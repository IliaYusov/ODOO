from odoo import fields, models


class ProjectRole(models.Model):
    _name = 'project.role'
    _description = 'Project Role'
    _order = 'sequence, id'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name, company_id)', 'Role with the same name already exists.'),
    ]
