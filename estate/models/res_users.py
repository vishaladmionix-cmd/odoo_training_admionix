from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    estate_role = fields.Selection(
        string='Estate Role',
        selection=[
            ('sales_executive', 'Sales Executive'),
            ('sales_manager', 'Sales Manager'),
            ('purchase_officer', 'Purchase Officer'),
            ('purchase_manager', 'Purchase Manager'),
        ],
    )
