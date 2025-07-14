from odoo import api, fields, models, _


class HelpdeskTicketType(models.Model):
    _name = 'helpdesk.ticket.type'
    _description = 'Ticket Type'

    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color', default=0)
    stage_ids = fields.Many2many('helpdesk.ticket.stage', relation='helpdesk_ticket_stage_type_rel', column1='type_id',
                                 column2='stage_id')
    start_stage_id = fields.Many2one('helpdesk.ticket.stage', ondelete='set null', compute='_compute_start_stage_id',
                                     readonly=True, store=True)
    ticket_count = fields.Integer(compute='_compute_ticket_count')
    ticket_open_count = fields.Integer(compute='_compute_ticket_open_count')
    ticket_unassigned_count = fields.Integer(compute='_compute_ticket_unassigned_count')
    ticket_closed_count = fields.Integer(compute='_compute_ticket_closed_count')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'A type with the same name already exists.')
    ]

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    def _compute_ticket_count(self):
        group_data = self.env['helpdesk.ticket'].read_group([
            ('type_id', 'in', self.ids)
        ], ['type_id'], ['type_id'])
        mapped_data = {data['type_id'][0]: data['type_id_count'] for data in group_data}
        for rec in self:
            rec.ticket_count = mapped_data.get(rec.id, 0)

    def _compute_ticket_open_count(self):
        group_data = self.env['helpdesk.ticket'].read_group([
            ('type_id', 'in', self.ids),
            ('stage_id.fold', '=', False)
        ], ['type_id'], ['type_id'])
        mapped_data = {data['type_id'][0]: data['type_id_count'] for data in group_data}
        for rec in self:
            rec.ticket_open_count = mapped_data.get(rec.id, 0)

    def _compute_ticket_unassigned_count(self):
        group_data = self.env['helpdesk.ticket'].read_group([
            ('type_id', 'in', self.ids),
            ('stage_id.fold', '=', False),
            ('user_id', '=', False)
        ], ['type_id'], ['type_id'])
        mapped_data = {data['type_id'][0]: data['type_id_count'] for data in group_data}
        for rec in self:
            rec.ticket_unassigned_count = mapped_data.get(rec.id, 0)

    def _compute_ticket_closed_count(self):
        group_data = self.env['helpdesk.ticket'].read_group([
            ('type_id', 'in', self.ids),
            ('stage_id.fold', '=', True)
        ], ['type_id'], ['type_id'])
        mapped_data = {data['type_id'][0]: data['type_id_count'] for data in group_data}
        for rec in self:
            rec.ticket_closed_count = mapped_data.get(rec.id, 0)

    @api.depends('stage_ids', 'stage_ids.sequence')
    def _compute_start_stage_id(self):
        for rec in self:
            if rec.stage_ids:
                rec.start_stage_id = rec.stage_ids.sorted(key=lambda st: st.sequence)[0]
            else:
                rec.start_stage_id = False

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_view_tickets(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('helpdesk_mngmnt.helpdesk_ticket_action_tickets_by_type')
        return action
