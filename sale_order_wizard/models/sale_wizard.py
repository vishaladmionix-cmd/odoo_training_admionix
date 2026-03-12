from odoo import models,api,fields

class SaleOrderWizard(models.TransientModel):

    _name = "sale.wizard"
    _description = "Sale Order Wizard"

    order_line_id = fields.Many2many("sale.order.line", string="Order Lines", domain="[('order_id', '=', order_id)]")
    order_id = fields.Many2one("sale.order", string="Order")

    # Text Field
    customer_note = fields.Char(string="Customer Note")

    # Date Field
    expected_delivery_date = fields.Date(string="Expected Delivery Date")

    # Selection Field
    priority_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string="Priority Level")


    # Boolean Field
    is_urgent = fields.Boolean(string="Is Urgent")



    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')

        if active_id:
            res['order_id'] = active_id


        return res

    def action_apply(self):
        self.ensure_one()
        delete_line =self.order_line_id

        for rec in delete_line:
            new_order = self.env['sale.order'].create({
                'partner_id': self.order_id.partner_id.id,
            })
            rec.copy({'order_id':new_order.id})

        delete_line.unlink()
        return {'type': 'ir.actions.act_window_close',}
