# -*- coding: utf-8 -*-
{
    'name': "customer_invoice_report",

    'summary': "Customize Report",

    'description': """
    A report to display invoices and sale orders for specific customers in a given time period
    """,

    'author': "Huzaifa Elnaeem",
    'website': "huz.dark1@gmail.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report_template.xml',
        'report/invoice_wizard_rep_form.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
