from odoo import fields, models

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_open_jewellery_wizard(self):

        return {
            'name': 'Create Sale',
            'type': 'ir.actions.act_window',
            'res_model': 'jewellery.sale.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            }
        }