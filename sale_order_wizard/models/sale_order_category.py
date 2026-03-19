from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_value_category = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        string='Order Value Category',
    )

