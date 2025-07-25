from odoo import fields, models, _


class HelpdeskTicketStage(models.Model):
    _name = 'helpdesk.ticket.stage'
    _description = 'Ticket Stage'
    _order = 'sequence, id'

    active = fields.Boolean(default=True)
    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean(string='Folded in Kanban', help='Tickets in a folded stage are considered as closed.')
    type_ids = fields.Many2many('helpdesk.ticket.type', relation='helpdesk_ticket_stage_type_rel', column1='stage_id',
                                column2='type_id', string='Ticket Types', required=True)
    template_id = fields.Many2one('mail.template', string='Email Template',
                                  domain="[('model', '=', 'helpdesk.ticket')]",
                                  help='Email automatically sent to the customer when the ticket reaches this stage.')
    ticket_count = fields.Integer(compute='_compute_ticket_count')

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    def _compute_ticket_count(self):
        group_data = self.env['helpdesk.ticket'].read_group(
            [('stage_id', 'in', self.ids)],
            ['stage_id'],
            ['stage_id']
        )
        mapped_data = {d['stage_id'][0]: d['stage_id_count'] for d in group_data}
        for rec in self:
            rec.ticket_count = mapped_data.get(rec.id, 0)

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_tickets(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('helpdesk_mngmnt.helpdesk_ticket_action')
        action.update({
            'domain': [('stage_id', 'in', self.ids)],
            'context': {
                'default_stage_id': self.id,
            }
        })
        return action
