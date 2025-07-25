from odoo import api, fields, models


class Task(models.Model):
    _inherit = 'task.task'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', copy=False,
                                groups='helpdesk_mngmnt.helpdesk_group_user')
