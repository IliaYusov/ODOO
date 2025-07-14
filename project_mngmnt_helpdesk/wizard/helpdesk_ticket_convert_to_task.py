from odoo import api, fields, models, _


class HelpdeskTicketConvertWizard(models.TransientModel):
    _name = 'helpdesk.ticket.convert.to.task'
    _description = 'Convert Helpdesk Ticket To Task'

    project_id = fields.Many2one('project.project', string='Project', domain="[('stage_id.fold', '=', False)]",
                                 required=True)
    task_type_id = fields.Many2one('task.type', string='Task Type',
                                   domain="[('model_id.model', '=', 'project.project')]", required=True)
    stage_id = fields.Many2one('task.stage', string='Stage', compute='_compute_default_stage_id',
                               domain="[('task_type_id', '=', task_type_id)]", readonly=False, required=True,
                               store=True)

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends('task_type_id')
    def _compute_default_stage_id(self):
        for rec in self:
            rec.stage_id = rec.task_type_id.start_stage_id if rec.task_type_id.start_stage_id else False

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_convert(self):
        ticket_ids = self._get_tickets_to_convert()

        task_ids = self.env['task.task'].with_context(mail_create_nolog=True).create(
            [self._get_task_values(ticket) for ticket in ticket_ids]
        )

        for ticket, task in zip(ticket_ids, task_ids):
            ticket.message_post(body=_('Ticket converted into task %s', task._get_html_link()))
            task.message_post_with_view(
                'mail.message_origin_link',
                values={'self': task, 'origin': ticket},
                subtype_id=self.env.ref('mail.mt_note').id
            )

        action_vals = {
            'type': 'ir.actions.act_window',
            'res_model': 'task.task',
        }

        if len(task_ids) == 1:
            action_vals.update({
                'view_mode': 'form',
                'res_id': task_ids[0].id
            })
        else:
            action_vals.update({
                'name': _('Converted Tasks'),
                'view_mode': 'list,form',
                'domain': [('id', 'in', task_ids.ids)]
            })
        return action_vals

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _get_tickets_to_convert(self):
        ticket_ids = self.env.context.get('ticket_ids', [])
        return self.env['helpdesk.ticket'].browse(ticket_ids)

    def _get_task_values(self, ticket):
        return {
            'name': ticket.name,
            'description': ticket.description,
            'parent_ref': '%s,%d' % ('project.project', self.project_id.id),
            'parent_ref_type': 'project.project',
            'parent_ref_id': self.project_id.id,
            'stage_id': self.stage_id.id,
            'planned_date_begin': fields.Date.today(),
            'date_deadline': self.project_id.date_end,
            'ticket_id': ticket.id
        }
