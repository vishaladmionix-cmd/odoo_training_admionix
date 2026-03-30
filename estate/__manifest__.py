{
    'name': 'Real Estate',
    'version': '19.0.1.0.0',
    'category': 'Real Estate',
    'summary': 'Manage properties, offers and sales',
    'author': 'ADmionix',
    'depends': ['base', 'mail', 'sale', 'crm', 'purchase'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/estate_property_view_inherit.xml',
        'views/sale_order_view_inherit.xml',
        'views/purchase_order_view_inherit.xml',
        'views/menu.xml',
        'views/res_user_view.xml',
        'data/cron.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
