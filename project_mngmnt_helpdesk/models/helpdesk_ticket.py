from odoo import models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_convert_to_task(self):
        return {
            'name': _('Convert To Task'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket.convert.to.task',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                **self.env.context,
                'ticket_ids': self.ids,
                'dialog_size': 'medium'
            }
        }
