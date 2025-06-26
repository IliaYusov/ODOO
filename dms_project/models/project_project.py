from odoo import api, models


class Project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'dms.document.mixin']

    @api.model
    def _init_project_document_directory(self):
        self.search([('directory_id', '=', False)])._create_project_directory()

    # ------------------------------------------------------
    # DMS.DOCUMENT.MIXIN
    # ------------------------------------------------------

    # TODO: сделать настройку с дефолтным каталогом в модуле?
    def _get_document_directory(self):
        return self.directory_id or self.env.ref('dms_project.dms_directory_project_directory')

    def _get_document_partner(self):
        return self.partner_id

    # ------------------------------------------------------
    # CRUD
    # ------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Project, self).create(vals_list)

        [rec._create_project_directory() for rec in records.filtered(lambda pr: not pr.directory_id)]

        return records

    def write(self, vals):
        if not vals.get('directory_id'):
            [rec._create_project_directory() for rec in self.filtered(lambda pr: not pr.directory_id)]

        res = super(Project, self).write(vals)
        if res and vals.get('partner_id'):
            [rec._move_files_to_partner() for rec in self]
        return res

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------

    def action_open_files(self):
        self.ensure_one()
        action_vals = super(Project, self).action_open_files()
        return action_vals

    # ------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------

    def _create_project_directory(self):
        for rec in self:
            # TODO: сделать настройку с дефолтным каталогом в модуле?
            directory = self.env['dms.directory'].create({
                'name': rec.name,
                'parent_id': self.env.ref('dms_project.dms_directory_project_directory').id
            })
            rec.write({'directory_id': directory.id})

    def _move_files_to_partner(self):
        files = self.env['dms.document'].sudo().search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
            ('partner_id', '!=', self.partner_id.id)
        ])
        if files:
            files.write({'partner_id': self.partner_id.id})
