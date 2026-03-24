{
    'name': 'CRM Opportunity Extend',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Adds Candidate Name and Job Profile to CRM Leads',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
}