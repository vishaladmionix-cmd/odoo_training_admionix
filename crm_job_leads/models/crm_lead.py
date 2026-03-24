from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    candidate_name = fields.Char(
        required=True,
        tracking=True,
        index=True
    )

    job_profile = fields.Selection(
        selection=[
            ('software_engineer', 'Software Engineer'),
            ('business_analyst',  'Business Analyst'),
            ('project_manager',   'Project Manager'),
            ('odoo_developer',    'Odoo Developer'),
            ('sales_executive',   'Sales Executive'),
            ('hr_manager',        'HR Manager'),
            ('data_analyst',      'Data Analyst'),
            ('other',             'Other'),
        ],
        default='other',
        tracking=True,
        index=True
    )