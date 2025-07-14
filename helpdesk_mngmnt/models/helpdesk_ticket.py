from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

PRIORITIES = [
    ('0', 'Not set'),
    ('1', 'Lowest'),
    ('2', 'Low'),
    ('3', 'Medium'),
    ('4', 'High'),
    ('5', 'Highest'),
]


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['portal.mixin', 'mail.thread.cc']
    _check_company_auto = True

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]

        if self.env.context.get('default_type_id'):
            search_domain = ['|', ('type_ids', 'in', self.env.context['default_type_id'])] + search_domain

        return stages.search(search_domain, order=order)

    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user)
    code = fields.Char(string='Code', copy=False, default=lambda self: _('New'), readonly=True, required=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Html(string='Description', sanitize_attributes=False)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    module_id = fields.Many2one('ir.model', string='Module')

    priority = fields.Selection(PRIORITIES, string='Priority', default='3', tracking=True)
    type_id = fields.Many2one('helpdesk.ticket.type', string='Type', copy=True, index=True, ondelete='restrict',
                              required=True, tracking=True)
    stage_id = fields.Many2one('helpdesk.ticket.stage', string='Stage', copy=True, depends=['type_id'],
                               group_expand='_read_group_stage_ids', index=True, ondelete='restrict', tracking=True)

    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', copy=False, tracking=True)
    user_id = fields.Many2one('res.users', string='Assigned', check_company=True, index=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', copy=True, tracking=True, index=True)
    date_assign = fields.Datetime(string='Assign Date', copy=False)
    date_closed = fields.Datetime(string='Date Closed', index=True, copy=False)

    attachment_count = fields.Integer(compute='_compute_attachment_count', string='Attachments')
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    def _compute_attachment_count(self):
        for ticket in self:
            ticket.attachment_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', ticket.id)
            ])

    def _compute_task_count(self):
        for ticket in self:
            ticket.task_count = self.env['task.task'].search_count([
                ('parent_id', '=', False),
                ('parent_ref_type', '=', self._name),
                ('parent_ref_id', '=', ticket.id)
            ])

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('type_id', False):
                type_id = self.env['helpdesk.ticket.type'].browse(vals['type_id'])
                if type_id and type_id.start_stage_id:
                    vals['stage_id'] = type_id.start_stage_id.id
                else:
                    raise ValidationError(
                        _("Cannot create ticket of type '%(type_name)s': This type have no start stage defined!") % {
                            'type_name': type_id.name})
            if vals.get('user_id'):
                vals['assign_date'] = fields.Datetime.now()

            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or _('New')

        return super(HelpdeskTicket, self).create(vals_list)

    def write(self, vals):
        if vals.get('user_id') and not self.date_assign:
            vals['assign_date'] = fields.Datetime.now()

        res = super(HelpdeskTicket, self)
        return res

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_attachments(self):
        self.ensure_one()
        return {
            'name': _('Attachments'),
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id),
            'help': """
                <p class="o_view_nocontent_smiling_face">%s</p>
                """ % _("Add attachments for this ticket")
        }
