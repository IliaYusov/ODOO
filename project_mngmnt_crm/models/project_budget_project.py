from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = 'project_budget.projects'

    project_count = fields.Integer(compute='_compute_project_data', string='Project Count',
                                   groups='project_mngmnt.project_group_user')
    project_ids = fields.One2many('project.project', 'opportunity_id', string='Projects', copy=False,
                                  groups='project_mngmnt.project_group_user')

    @api.depends('project_ids')
    def _compute_project_data(self):
        for rec in self:
            rec.project_count = len(rec.project_ids)

    def action_open_projects(self):
        self.ensure_one()
        action_vals = {
            'name': _('Projects'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'kanban,tree,form,calendar',
            'domain': [
                ('opportunity_id', '=', self.id)
            ],
            'context': {
                'default_opportunity_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_project_manager_id': self.project_manager_id.id
            },
            'help': """
                <p class="o_view_nocontent_smiling_face">%s</p>
                <p>%s</p>
            """ % (_('Create a new quotation, the first step of a new sale!'),
                   _('Once the quotation is confirmed, it becomes a sales order.'))
        }
        return action_vals
