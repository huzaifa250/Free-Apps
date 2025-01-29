# -*- coding: utf-8 -*-
{
    'name': "test_dev",

    'summary': "Track Customer Purchases/ development with odoo 17",

    'description': """
    	Track Customer Orders and Give prize ex discont if he/she bought same product
	3 times or more in the same month
    """,

    'author': "Huzaifa Elnaeem",
    'website': "huz.dark1@gmail.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/customer_purchase_tracker_view.xml',
        'report/purchase_tarcker_report_template.xml',
        'report/purchase_tracker_report_action.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
