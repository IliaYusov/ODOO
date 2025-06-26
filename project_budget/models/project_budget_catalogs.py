from ast import literal_eval
from odoo import models, fields, api
from odoo.tools.misc import get_lang


class vat_attribute(models.Model):  # TODO удалить после миграции на tax_id
    _name = 'project_budget.vat_attribute'
    _description = "project_vat attribute"
    name = fields.Char(string="vat_attribute name", required=True, translate=True)
    code = fields.Char(string="vat_attribute code", required=True)
    percent = fields.Float(string="vat_percent", required=True, default=0)
    descr = fields.Char(string="vat_attribute description", translate=True)
    is_prohibit_selection = fields.Boolean(string="is prohibit selection in projects", default=False)


class tender_current_status(models.Model):
    _name = 'project_budget.tender_current_status'
    _description = "tender current status"
    name = fields.Char(string="current status name", required=True, translate=True)
    code = fields.Char(string="current status code", required=True)
    descr = fields.Char(string="current status description", translate=True)
    highlight = fields.Boolean(string="highlight", default=False)


class tender_comments_type(models.Model):
    _name = 'project_budget.tender_comments_type'
    _description = "tender comments type"
    name = fields.Char(string="comment type name", required=True, translate=True)
    code = fields.Char(string="comment type code", required=True)
    descr = fields.Char(string="comment type description", translate=True)
