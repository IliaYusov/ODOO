from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    code = fields.Char(readonly=False)
    type_id = fields.Many2one('project.type', string='Project Type', copy=True, ondelete='restrict', tracking=True)
