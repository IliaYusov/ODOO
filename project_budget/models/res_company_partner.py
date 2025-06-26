from odoo import api, fields, models, _


# TODO: перенести функционал в новое приложение company_partner
class ResCompanyPartner(models.Model):
    _name = 'res.company.partner'
    _description = 'Company Partner'
    _rec_names_search = ['name', 'vat']

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 domain="['&', ('is_company', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 ondelete='restrict', required=True)
    name = fields.Char(related='partner_id.name', index=True, readonly=True, store=True)
    vat = fields.Char(related='partner_id.vat', index=True, readonly=True, store=True)
    type_id = fields.Many2one('res.company.partner.type', string='Partner Type', ondelete='restrict')
    grade_id = fields.Many2one('res.company.partner.grade', string='Partner Level', ondelete='restrict')
    active = fields.Boolean(string='Active', default=True)

    project_ids = fields.One2many('project_budget.projects', 'company_partner_id', string='Projects',
                                  domain="[('budget_state', '=', 'work'), ('company_id', '=', company_id)]")
    project_count = fields.Integer(compute='_compute_project_count')

    def name_get(self):
        res = []
        for rec in self:
            name = rec.name
            name += '%s' % ' [' + rec.grade_id.name + ']' if rec.grade_id else ''

            if rec.env.context.get('show_vat') and rec.vat:
                name = "%s ‒ %s" % (name, rec.vat)

            res += [(rec.id, name)]
        return res

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('project_ids')
    def _compute_project_count(self):
        for record in self:
            record.project_count = len(record.project_ids)

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_project(self):
        self.ensure_one()
        return {
            'name': _('Projects'),
            'domain': [
                ('id', 'in', self.project_ids.ids)
            ],
            'res_model': 'project_budget.projects',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'context': {
                'create': False,
                'edit': False,
                'delete': False
            },
            'help': """
                <p class="o_view_nocontent_smiling_face">%s</p>
                """ % _("No partner projects found.")
        }
