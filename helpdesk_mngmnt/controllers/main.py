import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request
from odoo.tools import plaintext2html

_logger = logging.getLogger(__name__)


class HelpdeskTicketController(http.Controller):

    @http.route('/helpdesk/ticket/new', type='http', auth='user', website=True)
    def submit_ticket(self, **kw):
        session_info = request.env['ir.http'].session_info()
        types = request.env['helpdesk.ticket.type'].search([])
        email = request.env.user.email
        name = request.env.user.name
        return request.render(
            'helpdesk_mngmnt.portal_helpdesk_ticket_submit_form',
            {
                'types': types,
                'email': email,
                'name': name,
                'max_upload_size': session_info['max_file_upload_size']
            }
        )

    @http.route("/helpdesk/ticket/submitted", type='http', auth='user', website=True, csrf=True)
    def submitted_ticket(self, **kw):
        vals = self._prepare_submit_ticket_vals(**kw)
        new_ticket = request.env['helpdesk.ticket'].sudo().create(vals)
        new_ticket.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        # if kw.get("attachment"):
        #     for c_file in request.httprequest.files.getlist("attachment"):
        #         data = c_file.read()
        #         if c_file.filename:
        #             request.env["ir.attachment"].sudo().create(
        #                 {
        #                     "name": c_file.filename,
        #                     "datas": base64.b64encode(data),
        #                     "res_model": "helpdesk.ticket",
        #                     "res_id": new_ticket.id,
        #                 }
        #             )
        return werkzeug.utils.redirect(f"/helpdesk/ticket/{new_ticket.id}")

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _prepare_submit_ticket_vals(self, **kw):
        type = http.request.env['helpdesk.ticket.type'].browse(
            int(kw.get('type'))
        )
        # company = type.company_id or http.request.env.company
        company = http.request.env.company
        vals = {
            'company_id': http.request.env.company.id,
            'type_id': type.id,
            'description': plaintext2html(kw.get('description')),
            'name': kw.get('subject'),
            # "attachment_ids": False,
            'partner_id': request.env.user.partner_id.company_id.id
        }
        # team = http.request.env['helpdesk.ticket.team']
        # if company.helpdesk_mgmt_portal_select_team and kw.get('team'):
        #     team = (
        #         http.request.env['helpdesk.ticket.team']
        #         .sudo()
        #         .search(
        #             [('id', '=', int(kw.get('team'))), ('show_in_portal', "=", True)]
        #         )
        #     )
        #     vals['team_id'] = team.id
        return vals
