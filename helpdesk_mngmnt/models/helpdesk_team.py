from odoo import api, fields, models


class Team(models.Model):
    _name = 'helpdesk.team'
    _description = 'Helpdesk Team'

    def _get_member_ids_domain(self):
        return "[('user_id.groups_id', 'in', %s), ('company_ids', 'in', company_id)]" \
            % self.env.ref('helpdesk_mngmnt.helpdesk_group_user').id

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    team_lead_id = fields.Many2one('res.users', string='Team Leader',
                                   domain=lambda self: [
                                       ('groups_id', 'in', self.env.ref('helpdesk_mngmnt.helpdesk_group_user').id)
                                   ])
    member_ids = fields.Many2many('res.users', string='Team Members', relation='helpdesk_team_user_rel',
                                  column1='team_id', column2='user_id', domain=_get_member_ids_domain)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    can_edit = fields.Boolean(compute='_compute_can_edit', default=True)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    def _compute_can_edit(self):
        for rec in self:
            rec.can_edit = rec.active
