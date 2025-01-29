# -*- coding: utf-8 -*-
{
    'name': "test_dev",

    'summary': "Test Development with odoo 17",

    'description': """
    Any features or development needed will be done or test here
    """,

    'author': "Huzaifa Elnaeem",
    'website': "huz.learnchannel@gmail.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/customer_purchase_tracker_view.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
