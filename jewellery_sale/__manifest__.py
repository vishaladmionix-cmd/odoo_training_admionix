{
    'name': 'Jewellery Sale',
    'summary': 'Manage Jewellery Sales with Wizard',
    'author': 'ADmionix',
    'category': 'Jewellery',
    'version': '19.0.1.0.0',
    'depends': ['base', 'sale'],
    'data': [
                'security/ir.model.access.csv',
                'views/views.xml',
                'views/sale_order_view_inherit.xml',
                'wizard/jewellery_sale_wizard.xml',
    ],
    'installable': True,
    'application': True,
}