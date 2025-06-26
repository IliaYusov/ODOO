from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Document(models.Model):
    _inherit = 'document_flow.document'

    project_manager_id = fields.Many2one('hr.employee', string='Project Manager', check_company=True, copy=True,
                                         domain="[('company_id', '=', company_id)]", tracking=True)

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if not vals.get('date_from', False):
    #             raise UserError(_("The field 'Start Date' is required to validate this document."))
    #         if not vals.get('date_to', False):
    #             raise UserError(_("The field 'End Date' is required to validate this document."))
    #         if not vals.get('absence_type_id', False):
    #             raise UserError(_("The field 'Absence Type' is required to validate this document."))
    #
    #     records = super(Document, self).create(vals_list)
    #     return records
