from odoo import fields, models


class EstatePropertyExtension(models.Model):
    _inherit = 'estate.property'

    # These fields get ADDED to estate.property automatically
    property_category = fields.Selection([
        ('villa', 'Villa'),
        ('appartement', 'Appartement'),
        ('plot', 'Plot'),
        ('commercial', 'Commercial'),
    ], string='Category', default='villa')

    floor_number    = fields.Integer(string='Floor Number')
    has_pool        = fields.Boolean(string='Has Swimming Pool')
    maintenance_fee = fields.Float(string='Monthly Maintenance (Rs./month)')
    is_furnished    = fields.Boolean(string='Is Furnished', default=False)