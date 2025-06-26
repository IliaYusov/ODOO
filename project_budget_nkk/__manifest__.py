{
    'name': 'Project Budget NKK',
    'version': '1.3.2',
    'category': 'Project',
    'depends': ['project_budget', 'base_automation', 'account_budget_mngmnt'],
    'description': """
    """,
    'data': [
        'security/project_budget_groups.xml',
        'security/project_budget_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/project_budget_data.xml',
        'views/project_budget_project_supervisor_views.xml',
        'views/project_budget_project_type_views.xml',
        'views/project_budget_acceptance_flow_views.xml',
        'views/project_budget_cash_flow_views.xml',
        'views/project_budget_cost_flow_views.xml',
        'views/project_budget_plan_kam_supervisor_views.xml',
        'views/project_budget_technological_direction_views.xml',
        'views/project_budget_project_member_views.xml',
        'views/project_budget_project_views.xml',
        'report/project_budget_project_overdue_report_views.xml',
        'report/crm_holding_customer_report_views.xml',
        'wizard/project_budget_project_print_report_views.xml',
        'views/project_budget_menus.xml'
    ],
    'installable': True,
    'auto_install': ['project_budget'],
    'license': 'LGPL-3'
}
