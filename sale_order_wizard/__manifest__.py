{
    'name': 'Sale Order Wizard',
    'version': '19.0.1.0.0',
    'summary': 'Send confirmation email on Sale Order confirmation',
    'category': 'Sales',
    'author': 'My Company',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'hr', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/sale_order_wizard_views.xml',
        'views/sale_wizard.xml',
        'views/account_move_views.xml',
        'views/sale_order_category_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}



