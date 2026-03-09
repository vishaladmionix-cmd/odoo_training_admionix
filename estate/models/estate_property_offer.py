from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string = 'Price' , required=True)

    status = fields.Selection(
        string = 'Status',
        selection = [
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string = 'Buyer',
        required=True,
    )

    property_id = fields.Many2one(
        comodel_name='estate.property',
        string='Property',
        required=True,
    )

    partner_phone = fields.Char(
        string='Buyer Phone',
        related='partner_id.phone',
        readonly=True,
    )