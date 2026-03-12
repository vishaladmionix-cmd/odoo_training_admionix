from odoo import fields, models

class AccountMoveCustom(models.Model):
    _inherit = "account.move"

    custom_reference = fields.Char(string="Custom Reference")
    custom_note = fields.Text(string="Custom Note")