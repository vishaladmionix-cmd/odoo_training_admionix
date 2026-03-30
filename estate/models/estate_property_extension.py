from odoo import fields, models


class EstatePropertyExtension(models.Model):
    _inherit = 'estate.property'

    property_category = fields.Selection(
        string='Property Category',
        selection=[
            ('residential', 'Residential'),
            ('commercial', 'Commercial'),
            ('industrial', 'Industrial'),
            ('land', 'Land'),
        ],
    )
    floor_number = fields.Integer(string='Floor Number')
    has_pool = fields.Boolean(string='Has Pool')
    maintenance_fee = fields.Float(string='Maintenance Fee')
    is_furnished = fields.Boolean(string='Is Furnished')
