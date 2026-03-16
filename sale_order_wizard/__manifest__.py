# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Wizard',
    'version': '1.0',
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Uncategorized',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': '',
    'depends': ['base','sale','hr','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_wizard_views.xml',
        'views/sale_wizard.xml',
        'views/account_move_views.xml',
        'views/sale_order_category_view.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
