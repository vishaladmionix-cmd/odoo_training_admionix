from odoo import fields, models,api
from datetime import timedelta
from odoo.exceptions import ValidationError,UserError




class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Property Name', required=True ,tracking=True )

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

    expected_price = fields.Float(string='Expected Price', required=True , tracking=True )
    selling_price = fields.Float(string='Selling Price', tracking=True)
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

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count"
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_view_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
            'target': 'current',
        }

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
        tracking=True,
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

    def action_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled property cannot be sold.")
        self.state = 'sold'

        new_property = self.env['estate.property'].create({
            'name': self.name + ' (Re-listed)',
            'description': self.description,
            'postcode': self.postcode,
            'expected_price': self.expected_price,
            'bedrooms': self.bedrooms,
            'living_area': self.living_area,
            'state': 'new',
        })



    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold property cannot be cancelled.")
        self.state = 'cancelled'

    def action_view_accepted_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accepted Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [
                ('property_id', '=', self.id),
                ('status', '=', 'accepted')
            ],
            'context': {'default_property_id': self.id},
            'target': 'current',
        }