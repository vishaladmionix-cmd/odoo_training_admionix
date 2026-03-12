from odoo import api, fields, models

class SaleOrderCustom(models.Model):
    _inherit = "sale.order"

    # ✅ Add these two fields
    custom_reference = fields.Char(string="Custom Reference")
    custom_note = fields.Text(string="Custom Note")

    def action_open_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manage Sale Order',
            'res_model': 'sale.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            }
        }

    # ✅ This passes fields to invoice
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['custom_reference'] = self.custom_reference
        res['custom_note'] = self.custom_note
        return res