from odoo import fields, models,api
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From')

    validity = fields.Integer(
        string = 'Validity (days)',
        compute='_compute_validity',
        inverse='_inverse_validity',
        default = 90,
    )

    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_validity',
        inverse='_inverse_validity',
    )

    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    total_area = fields.Integer(
        string = 'Total Area (sqm)',
        compute='_compute_total_area',
        search = '_search_total_area',
        )

    def _search_total_area(self,operator,value):
        return [
            '|',
            ('living_area',operator,value),
            ('garden_area',operator,value),
        ]

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area



    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
    )


    property_type_id = fields.Many2one(
        comodel_name = 'estate.property.type',
        string='Property Type',
    )

    tag_ids = fields.Many2many(
        comodel_name = 'estate.property.tag',
        string='Tags',
    )

    offer_ids = fields.One2many(
        comodel_name = 'estate.property.offer',
        inverse_name = 'property_id',
        string = 'Offers',
    )

    buyer_id = fields.Many2one(
        comodel_name = 'res.partner',
        string='Buyer',
    )

    salesperson_id = fields.Many2one(
        comodel_name = 'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )

    @api.depends('date_availability', 'validity')
    def _compute_validity(self):
        for record in self:
            if record.date_availability:
                record.date_deadline = record.date_availability + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            if record.date_deadline:
                record.date_availability = record.date_deadline - timedelta(days = record.validity)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False