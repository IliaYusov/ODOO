from odoo import fields, models


class DocumentKind(models.Model):
    _name = 'document_flow.document.kind'
    _description = 'Document Kind'

    name = fields.Char(string='Name', copy=False, required=True)
    template_id = fields.Many2one('document_flow.document.kind.template', string='Template', copy=False, index=True,
                                  ondelete='cascade', required=True)
    type_id = fields.Many2one('document_flow.document.kind.type', string='Type', copy=False, index=True,
                              ondelete='cascade')
    sequence_id = fields.Many2one(related='template_id.sequence_id', string='Document Kind Sequence', copy=False,
                                  readonly=True)
    document_ids = fields.One2many('document_flow.document', 'kind_id', string='Documents')
    properties_definition = fields.PropertiesDefinition('Document Properties')
