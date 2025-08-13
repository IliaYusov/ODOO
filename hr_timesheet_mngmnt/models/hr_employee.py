from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    hourly_cost = fields.Monetary(string='Hourly Cost', default=0.0)
