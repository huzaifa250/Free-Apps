# -*- coding: utf-8 -*-
{
    'name': "Vacation calculation",

    'summary': """
        Calculate day price for the employee and total amount of vacation""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Huzaifa Elnaeem",
    'website': "huz.dark1@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_holidays', 'hr', 'hr_contract', 'base_accounting_kit', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vacation_calc_view.xml',
        # 'views/add_day_price_to_requset.xml',
        # 'views/add_day_price.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
