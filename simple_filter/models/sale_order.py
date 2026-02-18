from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_confirmed_orders(self):
        """
        Open Sales Orders filtered to confirmed ones.
        States: 'sale' = confirmed, 'done' = locked/done
        """
        return {
            "type": "ir.actions.act_window",
            "name": "Confirmed Orders (Custom Action)",
            "res_model": "sale.order",
            "view_mode": "kanban,tree,form",
            "domain": [("state", "in", ["sale", "done"])],
            "context": dict(self.env.context),
        }
