from odoo import fields, models


class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'
    _order = 'sequence, id'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban', default=False,
                          help='If enabled, this stage will be displayed as folded in the Kanban view of your projects.')
    company_ids = fields.Many2many('res.company', relation='project_stage_company_rel',
                                   column1='stage_id', column2='company_id', string='Companies',
                                   domain=lambda self: [('id', 'in', self.env.context.get('allowed_company_ids', []))])
