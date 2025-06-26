from odoo import fields, models


class DocumentEmployee(models.Model):
    _inherit = 'document_flow.document.employee'

    role_id = fields.Many2one('project.role', string='Project Role', ondelete='restrict', required=True)
