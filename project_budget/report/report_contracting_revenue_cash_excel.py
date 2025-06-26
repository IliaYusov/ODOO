from datetime import datetime
from odoo import models
from odoo.tools import date_utils


class ReportContractingRevenueCashExcel(models.AbstractModel):
    _name = 'report.project_budget.report_contracting_revenue_cash_excel'
    _description = 'report contracting revenue cash excel'
    _inherit = 'report.report_xlsx.abstract'

    def print_ctg(self, workbook, sheet, prj, row, col):

        row_format = workbook.add_format({
            'font_size': 10,
        })
        row_format_number = workbook.add_format({
            'font_size': 10,
            'num_format': '#,##0',
        })
        row_format_date = workbook.add_format({
            'font_size': 10,
            'num_format': 'dd.mm.yyyy',
        })

        sheet.write(row, col, prj.project_id, row_format)
        col += 1
        sheet.write(row, col, prj.step_project_number or '', row_format)
        col += 1
        sheet.write(row, col, prj.responsibility_center_id.name, row_format)
        col += 1

        if prj.order_ids:
            pn = ', '.join(cat.root_category_id.name if cat.root_category_id else cat.name for cat in prj.order_ids.line_ids.product_category_id)
            sheet.write(row, col, pn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        if prj.order_ids:
            rpn = ', '.join(cat.root_category_id.head_id.name if cat.root_category_id else cat.head_id.name for cat in prj.order_ids.line_ids.product_category_id if (cat.root_category_id.head_id if cat.root_category_id else cat.head_id))
            sheet.write(row, col, rpn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        sheet.write(row, col, prj.key_account_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.project_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.company_partner_id.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.essence_project or '', row_format)
        col += 1
        sheet.write(row, col, prj.stage_id.name, row_format)
        col += 1
        sheet.write(row, col, prj.profitability, row_format_number)
        col += 1
        sheet.write(row, col, prj.end_presale_project_month, row_format_date)
        col += 1
        sheet.write(row, col, 'Q' + str(date_utils.get_quarter_number(prj.end_presale_project_month)) + ' ' + str(prj.end_presale_project_month.year), row_format)
        col += 1
        sheet.write(row, col, prj.amount_total_in_company_currency, row_format_number)
        col += 1
        sheet.write(row, col, prj.comments or '', row_format)

    def print_rvn(self, workbook, sheet, prj, rvn, row, col, rvn_type):
        row_format = workbook.add_format({
            'font_size': 10,
        })
        row_format_number = workbook.add_format({
            'font_size': 10,
            'num_format': '#,##0',
        })
        row_format_date = workbook.add_format({
            'font_size': 10,
            'num_format': 'dd.mm.yyyy',
        })

        sheet.write(row, col, prj.project_id, row_format)
        col += 1
        if rvn_type == 'План':
            sheet.write(row, col, str(rvn.id) + 'П', row_format)
        else:
            sheet.write(row, col, str(rvn.id) + 'Ф', row_format)
        col += 1
        sheet.write(row, col, prj.step_project_number or '', row_format)
        col += 1
        sheet.write(row, col, prj.responsibility_center_id.name, row_format)
        col += 1

        if prj.order_ids:
            pn = ', '.join(cat.root_category_id.name if cat.root_category_id else cat.name for cat in prj.order_ids.line_ids.product_category_id)
            sheet.write(row, col, pn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        if prj.order_ids:
            rpn = ', '.join(cat.root_category_id.head_id.name if cat.root_category_id else cat.head_id.name for cat in prj.order_ids.line_ids.product_category_id if (cat.root_category_id.head_id if cat.root_category_id else cat.head_id))
            sheet.write(row, col, rpn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        sheet.write(row, col, prj.key_account_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.project_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.company_partner_id.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.essence_project or '', row_format)
        col += 1
        sheet.write(row, col, prj.stage_id.name, row_format)
        col += 1
        sheet.write(row, col, prj.profitability, row_format_number)
        col += 1
        sheet.write(row, col, prj.end_presale_project_month, row_format_date)
        col += 1
        sheet.write(row, col, prj.amount_total_in_company_currency, row_format_number)
        col += 1
        sheet.write(row, col, rvn.date, row_format_date)
        col += 1
        sheet.write(row, col, 'Q' + str(date_utils.get_quarter_number(rvn.date)) + ' ' + str(rvn.date.year), row_format)
        col += 1
        sheet.write(row, col, rvn.amount_in_company_currency, row_format_number)
        col += 1
        sheet.write(row, col, rvn_type, row_format)
        col += 1
        sheet.write(row, col, prj.comments or '', row_format)

    def print_csh(self, workbook, sheet, prj, csh, row, col, csh_type):
        row_format = workbook.add_format({
            'font_size': 10,
        })
        row_format_number = workbook.add_format({
            'font_size': 10,
            'num_format': '#,##0',
        })
        row_format_date = workbook.add_format({
            'font_size': 10,
            'num_format': 'dd.mm.yyyy',
        })

        sheet.write(row, col, prj.project_id, row_format)
        col += 1
        if csh_type == 'План':
            sheet.write(row, col, str(csh.id) + 'П', row_format)
        else:
            sheet.write(row, col, str(csh.id) + 'Ф', row_format)
        col += 1
        sheet.write(row, col, prj.step_project_number or '', row_format)
        col += 1
        sheet.write(row, col, prj.responsibility_center_id.name, row_format)
        col += 1

        if prj.order_ids:
            pn = ', '.join(cat.root_category_id.name if cat.root_category_id else cat.name for cat in prj.order_ids.line_ids.product_category_id)
            sheet.write(row, col, pn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        if prj.order_ids:
            rpn = ', '.join(cat.root_category_id.head_id.name if cat.root_category_id else cat.head_id.name for cat in prj.order_ids.line_ids.product_category_id if (cat.root_category_id.head_id if cat.root_category_id else cat.head_id))
            sheet.write(row, col, rpn, row_format)
        else:
            sheet.write(row, col, '', row_format)
        col += 1

        sheet.write(row, col, prj.key_account_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.project_manager_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.company_partner_id.partner_id.name or '', row_format)
        col += 1
        sheet.write(row, col, prj.essence_project or '', row_format)
        col += 1
        sheet.write(row, col, prj.stage_id.name, row_format)
        col += 1
        sheet.write(row, col, prj.profitability, row_format_number)
        col += 1
        sheet.write(row, col, prj.end_presale_project_month, row_format_date)
        col += 1
        sheet.write(row, col, prj.amount_total_in_company_currency, row_format_number)
        col += 1
        sheet.write(row, col, csh.date, row_format_date)
        col += 1
        sheet.write(row, col, 'Q' + str(date_utils.get_quarter_number(csh.date)) + ' ' + str(csh.date.year), row_format)
        col += 1
        sheet.write(row, col, csh.amount_in_company_currency, row_format_number)
        col += 1
        sheet.write(row, col, csh_type, row_format)
        col += 1

        if csh_type == 'План':
            frst_faf = prj.planned_acceptance_flow_ids.sorted('date')[:1]
            frst_fcf = prj.planned_cash_flow_ids.sorted('date')[:1]
        else:
            frst_faf = prj.fact_acceptance_flow_ids.sorted('date')[:1] or prj.planned_acceptance_flow_ids.sorted(
                'date')[:1]
            frst_fcf = prj.fact_cash_flow_ids.sorted('date')[:1]
        res = ''
        if frst_faf and frst_fcf:
            if frst_fcf.date <= frst_faf.date and frst_fcf.amount >= frst_faf.amount * (
                    1 + prj.tax_id.amount / 100):
                res = 'Предоплата 100%'
            elif frst_fcf.date <= frst_faf.date and frst_fcf.amount < frst_faf.amount * (
                    1 + prj.tax_id.amount / 100):
                res = 'Частичная предоплата'
            elif frst_fcf.date > frst_faf.date:
                res = 'Постоплата 100%'

        sheet.write(row, col, res, row_format)
        col += 1

        sheet.write(row, col, prj.comments or '', row_format)

    def print_worksheets(self, workbook, sheets, date_start, date_end):
        projects = self.env['project_budget.projects'].search([
            ('budget_state', '=', 'work'),
            '|', '&', ('step_status', '=', 'step'),
            ('step_project_parent_id.project_have_steps', '=', True),
            '&', ('step_status', '=', 'project'),
            ('project_have_steps', '=', False),
        ], order='project_id asc')

        row_ctg = row_rvn = row_csh = 0

        for prj in projects:
            if date_start <= prj.end_presale_project_month <= date_end:
                row_ctg += 1
                self.print_ctg(workbook, sheets['contracting'], prj, row_ctg, 0)

            for rvn in prj.planned_acceptance_flow_ids:
                if date_start <= rvn.date <= date_end:
                    row_rvn += 1
                    self.print_rvn(workbook, sheets['revenue'], prj, rvn, row_rvn, 0, 'План')
            for rvn in prj.fact_acceptance_flow_ids:
                if date_start <= rvn.date <= date_end:
                    row_rvn += 1
                    self.print_rvn(workbook, sheets['revenue'], prj, rvn, row_rvn, 0, 'Факт')

            for csh in prj.planned_cash_flow_ids:
                if date_start <= csh.date <= date_end:
                    row_csh += 1
                    self.print_csh(workbook, sheets['cash'], prj, csh, row_csh, 0, 'План')
            for csh in prj.fact_cash_flow_ids:
                if date_start <= csh.date <= date_end:
                    row_csh += 1
                    self.print_csh(workbook, sheets['cash'], prj, csh, row_csh, 0, 'Факт')
        sheets['contracting'].add_table(0, 0, row_ctg, 15, {
            'columns': [
                {'header': 'ID проекта'},
                {'header': 'Номер этапа проекта'},
                {'header': 'Центр ответственности'},
                {'header': 'ПН'},
                {'header': 'Ответственный РПН'},
                {'header': 'КАМ'},
                {'header': 'Руководитель проекта'},
                {'header': 'Заказчик'},
                {'header': 'Партнер'},
                {'header': 'Наименование'},
                {'header': 'Этап'},
                {'header': 'Рентабельность'},
                {'header': 'Дата контрактования'},
                {'header': 'Квартал контрактования'},
                {'header': 'Сумма контрактования'},
                {'header': 'Комментарий к проекту'}
            ]
        })
        sheets['revenue'].add_table(0, 0, row_rvn, 19, {
            'columns': [
                {'header': 'ID проекта'},
                {'header': 'ID ВВ'},
                {'header': 'Номер этапа проекта'},
                {'header': 'Центр ответственности'},
                {'header': 'ПН'},
                {'header': 'Ответственный РПН'},
                {'header': 'КАМ'},
                {'header': 'Руководитель проекта'},
                {'header': 'Заказчик'},
                {'header': 'Партнер'},
                {'header': 'Наименование'},
                {'header': 'Этап'},
                {'header': 'Рентабельность'},
                {'header': 'Дата контрактования'},
                {'header': 'Сумма контрактования'},
                {'header': 'Дата ВВ'},
                {'header': 'Квартал ВВ'},
                {'header': 'Сумма ВВ'},
                {'header': 'Тип'},
                {'header': 'Комментарий к проекту'}
            ]
        })
        sheets['cash'].add_table(0, 0, row_csh, 20, {
            'columns': [
                {'header': 'ID проекта'},
                {'header': 'ID ПДС'},
                {'header': 'Номер этапа проекта'},
                {'header': 'Центр ответственности'},
                {'header': 'ПН'},
                {'header': 'Ответственный РПН'},
                {'header': 'КАМ'},
                {'header': 'Руководитель проекта'},
                {'header': 'Заказчик'},
                {'header': 'Партнер'},
                {'header': 'Наименование'},
                {'header': 'Этап'},
                {'header': 'Рентабельность'},
                {'header': 'Дата контрактования'},
                {'header': 'Сумма контрактования'},
                {'header': 'Дата ПДС'},
                {'header': 'Квартал ПДС'},
                {'header': 'Сумма ПДС'},
                {'header': 'Тип'},
                {'header': 'Тип оплаты'},
                {'header': 'Комментарий к проекту'}
            ]
        })

    def generate_xlsx_report(self, workbook, data, budgets):
        date_start = datetime.strptime(data['date_start'], '%Y-%m-%d').date()
        date_end = datetime.strptime(data['date_end'], '%Y-%m-%d').date()

        sheets = {
            'contracting': workbook.add_worksheet('Контракт'),
            'revenue': workbook.add_worksheet('ВВ'),
            'cash': workbook.add_worksheet('ПДС'),
        }

        self.print_worksheets(workbook, sheets, date_start, date_end)
