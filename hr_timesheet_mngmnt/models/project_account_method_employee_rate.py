from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class AccountMethodEmployeeRate(models.Model):
    _name = 'project.account.method.employee.rate'
    _description = 'Project Account Method Employee Rate'
    _order = 'sequence, id'

    name = fields.Char(string='Name', copy=True, required=True, translate=True)
    sequence = fields.Integer(default=1)
    expression = fields.Text(string='Expression', copy=True, required=True)
    manual_hourly_cost = fields.Boolean(string='Manual hourly cost')
    active = fields.Boolean('Active', default=True)

    @api.constrains('expression')
    def _verify_expression(self):
        for rec in self.filtered('expression'):
            msg = test_python_expr(expr=rec.expression.strip(), mode='exec')
            if msg:
                raise ValidationError(msg)
