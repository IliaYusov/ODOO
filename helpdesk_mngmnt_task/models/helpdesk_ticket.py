from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    task_count = fields.Integer(compute='_compute_task_count')

    def _compute_task_count(self):
        group_data = self.env['task.task'].read_group([
            ('ticket_id', 'in', self.ids)
        ], ['ticket_id'], ['ticket_id'])
        mapped_data = {data['ticket_id'][0]: data['ticket_id_count'] for data in group_data}
        for rec in self:
            rec.task_count = mapped_data.get(rec.id, 0)
