# from odoo import fields, models, api
#
#
# class JewellerySaleWizard(models.TransientModel):
#     _name = 'jewellery.sale.wizard'
#     _description = 'Jewellery Sale Wizard'
#
#     sale_order_id = fields.Many2one(
#         'sale.order',
#         string='Sale Order',
#         required=True
#     )
#
#     product_line_id = fields.Many2many(
#          'sale.order.line',
#         string='Order Lines',
#         domain="[('order_id','=',sale_order_id)]"
#     )
#     # product_ids = fields.Many2many(
#     #     'sale.order.line',
#     #     string='Order Lines',
#     #     domain="[('order_id','=',sale_order_id)]"
#     # )
#
#     def action_apply(self):
#         self.ensure_one()
#         delete_line = self.product_line_id
#
#         for rec in delete_line:
#             new_order = self.env['sale.order'].create({
#                 'partner_id': self.sale_order_id.partner_id.id,
#             })
#
#             rec.copy({
#                 'order_id': new_order.id
#             })
#
#         delete_line.unlink()
#
#         return {'type': 'ir.actions.act_window_close'}









from odoo import models, fields

class JewellerySaleWizard(models.TransientModel):
    _name = 'jewellery.sale.wizard'
    _description = 'Jewellery Sale Wizard'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True
    )

    product_line_id = fields.Many2one(
        'sale.order.line',
        string='Order Line',
        domain="[('order_id','=',sale_order_id)]"
    )

    def action_apply(self):
        self.ensure_one()

        line = self.product_line_id

        new_order = self.env['sale.order'].create({
            'partner_id': self.sale_order_id.partner_id.id,
        })

        line.copy({'order_id': new_order.id})
        line.unlink()

        return {'type': 'ir.actions.act_window_close'}