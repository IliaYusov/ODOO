from odoo import models
from odoo.tools import date_utils


class report_projects_rawdata_excel(models.AbstractModel):
    _name = 'report.project_budget.report_projects_rawdata_excel'
    _description = 'project_budget.report_projects_rawdata_excel'
    _inherit = 'report.report_xlsx.abstract'

    def printworksheet(self, workbook, budget, namesheet):
        global strYEAR

        report_name = budget.name
        # One sheet by partner
        sheet = workbook.add_worksheet(namesheet)
        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        head_format = workbook.add_format({
            'bold': True,
            'italic': True,
            'border': 1,
            'font_name': 'Arial',
            'font_size': 11,
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#3265a5',
            'color': '#ffffff'
        })

        row_format_date_month = workbook.add_format({
            'border': 1,
            'font_size': 11,
            'font_name': 'Times New Roman'
            # 'num_format': 14
            #                'text_wrap' : True,
            #                'align': 'center',
            #                'valign': 'vcenter',
            #                'fg_color': '#3265a5',
        })

        row_format_date_month.set_num_format('mmmm yyyy')
        row_format = workbook.add_format({
            'border': 1,
            'font_size': 11,
            'font_name': 'Times New Roman'
            #                'text_wrap' : True,
            #                'align': 'center',
            #                'valign': 'vcenter',
            #                'fg_color': '#3265a5',
        })
        row_format_number = workbook.add_format({
            'border': 1,
            'font_size': 11,
            'num_format': '#,##0.00',
            'font_name': 'Times New Roman'
        })
        date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})

        row = 0
        column = 0
        sheet.write_string(row, column, 'Компания', row_format)
        column += 1
        sheet.write_string(row, column, 'project_id', row_format)
        column += 1
        sheet.write_string(row, column, 'step_id', row_format)
        column += 1
        sheet.write_string(row, column, 'Статус согласования', row_format)
        column += 1
        sheet.write_string(row, column, 'Статус проекта', row_format)
        column += 1
        sheet.write_string(row, column, 'Номер этапа проекта из AXAPTA', row_format)
        column += 1
        sheet.write_string(row, column, 'Это этап', row_format)
        column += 1
        sheet.write_string(row, column, 'Состояние бюджета', row_format)
        column += 1
        sheet.write_string(row, column, 'Валюта проекта', row_format)
        column += 1
        sheet.write_string(row, column, 'Проектный офис', row_format)
        column += 1
        sheet.write_string(row, column, 'Куратор', row_format)
        column += 1
        sheet.write_string(row, column, 'КАМ', row_format)
        column += 1
        sheet.write_string(row, column, 'Руководитель проекта', row_format)
        column += 1
        sheet.write_string(row, column, 'Отрасль', row_format)
        column += 1
        sheet.write_string(row, column, 'Заказчик/организация', row_format)
        column += 1
        sheet.write_string(row, column, 'Наименование проекта', row_format)
        column += 1
        sheet.write_string(row, column, 'Юрлицо, подписывающее договор от НКК', row_format)
        column += 1
        sheet.write_string(row, column, 'Комментарий к проекту', row_format)
        column += 1
        sheet.write_string(row, column, 'Технологическое направление', row_format)
        column += 1
        sheet.write_string(row, column, 'Тип проекта', row_format)
        column += 1
        sheet.write_string(row, column, 'Номер договора (проекта)', row_format)
        column += 1
        sheet.write_string(row, column, 'Квартал контрактования', row_format)
        column += 1
        sheet.write_string(row, column, 'Дата контрактования', row_format_date_month)
        column += 1
        sheet.write_string(row, column, 'Квартал последней отгрузки', row_format)
        column += 1
        sheet.write_string(row, column, 'Последняя отгрузка', row_format_date_month)
        column += 1
        sheet.write_string(row, column, 'Признак НДС', row_format)
        column += 1
        sheet.write_string(row, column, 'Сумма выручки', row_format_number)
        column += 1
        sheet.write_string(row, column, "Сумма выручки с НДС", row_format_number)
        column += 1
        sheet.write_string(row, column, "Сумма прогноза актирования без НДС", row_format_number)
        column += 1
        sheet.write_string(row, column, "Сумма прогноза ПДС с НДС", row_format_number)
        column += 1
        sheet.write_string(row, column, "Выручка от реализации работ(услуг)", row_format_number)
        column += 1
        sheet.write_string(row, column, "Выручка от реализации товара", row_format_number)
        column += 1
        sheet.write_string(row, column, "Себестоимость проекта", row_format_number)
        column += 1
        sheet.write_string(row, column, "Себестоимость товаров", row_format_number)
        column += 1
        sheet.write_string(row, column, "Работы собственные (ФОТ)", row_format_number)
        column += 1
        sheet.write_string(row, column, "Работы сторонние (субподряд)", row_format_number)
        column += 1
        sheet.write_string(row, column, "Премии по итогам проекта", row_format_number)
        column += 1
        sheet.write_string(row, column, "Транспортные расходы", row_format_number)
        column += 1
        sheet.write_string(row, column, "Командировочные расходы", row_format_number)
        column += 1
        sheet.write_string(row, column, "Представительские расходы", row_format_number)
        column += 1
        sheet.write_string(row, column, "Налоги на ФОТ и премии", row_format_number)
        column += 1
        sheet.write_string(row, column, "Расходы на гарант. обслуж.", row_format_number)
        column += 1
        sheet.write_string(row, column, "РКО прочие", row_format_number)
        column += 1
        sheet.write_string(row, column, "Прочие расходы", row_format_number)
        column += 1
        sheet.write_string(row, column, "Маржа", row_format_number)
        column += 1
        sheet.write_string(row, column, "Рентабельность", row_format_number)
        column += 1
        sheet.write_string(row, column, "Вероятность проекта", row_format_number)

        cur_budget_projects = self.env['project_budget.projects'].search([
            ('commercial_budget_id', '=', budget.id),
            '|', '&', ('step_status', '=', 'step'),
            ('step_project_parent_id.project_have_steps', '=', True),
            '&', ('step_status', '=', 'project'),
            ('project_have_steps', '=', False)
        ]).sorted(key=lambda
            r: r.project_id if r.step_status == 'project' else r.step_project_parent_id.project_id + r.project_id)

        for spec in cur_budget_projects:
            row += 1
            column = 0
            sheet.write_string(row, column, spec.company_id.name, row_format)
            column += 1
            if spec.step_status == 'project':
                sheet.write_string(row, column, spec.project_id, row_format)
            elif spec.step_status == 'step':
                sheet.write_string(row, column, spec.step_project_parent_id.project_id, row_format)
            column += 1
            sheet.write_string(row, column, spec.step_project_parent_id.project_id if spec.step_status == 'step' else '', row_format)
            column += 1
            sheet.write_string(row, column, spec.approve_state, row_format)
            column += 1
            sheet.write_string(row, column, spec.project_status, row_format)
            column += 1
            sheet.write_string(row, column, spec.step_project_number or '', row_format)
            column += 1
            if spec.step_status == 'step':
                sheet.write_string(row, column, "True", row_format)
            else:
                sheet.write_string(row, column, "False", row_format)
            column += 1
            sheet.write_string(row, column, spec.budget_state, row_format)
            column += 1
            sheet.write_string(row, column, spec.currency_id.name, row_format)
            column += 1
            sheet.write_string(row, column, spec.responsibility_center_id.name, row_format)
            column += 1
            sheet.write_string(row, column, spec.project_supervisor_id.name or '', row_format)
            column += 1
            sheet.write_string(row, column, spec.key_account_manager_id.name, row_format)
            column += 1
            sheet.write_string(row, column, (spec.project_manager_id.name or ""), row_format)
            column += 1
            sheet.write_string(row, column, spec.industry_id.name, row_format)
            column += 1
            # sheet.write_string(row, column, spec.customer_status_id.name, row_format)
            # column += 1
            sheet.write_string(row, column, spec.partner_id.name, row_format)
            column += 1
            sheet.write_string(row, column, spec.essence_project or '', row_format)
            column += 1
            sheet.write_string(row, column, spec.signer_id.name, row_format)
            column += 1
            sheet.write_string(row, column, spec.comments or spec.step_project_parent_id.comments or '', row_format)
            column += 1
            sheet.write_string(row, column, spec.technological_direction_id.name or '', row_format)
            column += 1
            sheet.write_string(row, column, spec.project_type_id.name or '', row_format)
            column += 1
            sheet.write_string(row, column, spec.dogovor_number or spec.step_project_parent_id.dogovor_number or '', row_format)
            column += 1
            sheet.write_string(row, column, 'Q%d %d' % (date_utils.get_quarter_number(spec.end_presale_project_month), spec.end_presale_project_month.year), row_format)
            column += 1
            sheet.write_datetime(row, column, spec.end_presale_project_month, row_format_date_month)
            column += 1
            sheet.write_string(row, column, 'Q%d %d' % (date_utils.get_quarter_number(spec.end_sale_project_month), spec.end_sale_project_month.year) if spec.end_sale_project_month else '', row_format)
            column += 1
            sheet.write(row, column, spec.end_sale_project_month or '', row_format_date_month)
            column += 1
            sheet.write_string(row, column, spec.tax_id.name or '', row_format)
            column += 1
            sheet.write_number(row, column, spec.amount_untaxed_in_company_currency, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.amount_total_in_company_currency, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.planned_amount_untaxed_acts, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.planned_amount_total_cash_flow, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.revenue_from_the_sale_of_works, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.revenue_from_the_sale_of_goods, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.cost_price_in_company_currency, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.cost_of_goods, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.own_works_fot, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.third_party_works, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.awards_on_results_project, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.transportation_expenses, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.travel_expenses, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.representation_expenses, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.taxes_fot_premiums, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.warranty_service_costs, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.rko_other, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.other_expenses, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.margin_in_company_currency, row_format_number)
            column += 1
            sheet.write_number(row, column, spec.profitability, row_format_number)
            column += 1
            sheet.write_string(row, column, spec.stage_id.code, row_format_number)

    def generate_xlsx_report(self, workbook, data, budgets):
        global strYEAR
        strYEAR = str(data['year'])
        commercial_budget_id = data['commercial_budget_id']
        budget = self.env['project_budget.commercial_budget'].search([('id', '=', commercial_budget_id)])

        self.printworksheet(workbook, budget, 'raw_data')
