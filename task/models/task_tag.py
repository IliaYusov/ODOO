from random import randint

from odoo import fields, models


class TaskTag(models.Model):
    _name = 'task.tag'
    _description = 'Task Tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color,
                           help='Transparent tags are not visible in the kanban view of your projects and tasks.')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A tag with the same name already exists.'),
    ]
