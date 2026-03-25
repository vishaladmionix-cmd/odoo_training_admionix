{
    'name': 'Library Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage books, members and borrowing',
    'author': 'My Company',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/mail_template.xml',
        'views/library_model_view.xml',
        'views/library_member_view.xml',
        'views/library_borrow_view.xml',
        'views/server_actions.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
}
