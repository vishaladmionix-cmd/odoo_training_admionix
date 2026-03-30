from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Property Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From')

    validity = fields.Integer(
        string='Validity (days)',
        compute='_compute_validity',
        inverse='_inverse_validity',
        store=True,
    )
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_validity',
        inverse='_inverse_validity',
        store=True,
    )

    expected_price = fields.Float(string='Expected Price', required=True, tracking=True)
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
        string='Total Area (sqm)',
        compute='_compute_total_area',
        search='_search_total_area',
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count"
    )
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
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Type')
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string='Offers')
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer')
    salesperson_id = fields.Many2one(comodel_name='res.users', string='Salesperson', default=lambda self: self.env.user)

    # ───── COMPUTE METHODS ─────

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def _search_total_area(self, operator, value):
        return ['|', ('living_area', operator, value), ('garden_area', operator, value)]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('date_availability', 'date_deadline')
    def _compute_validity(self):
        for record in self:
            if record.date_availability and record.date_deadline:
                delta = record.date_deadline - record.date_availability
                record.validity = delta.days
            elif record.date_deadline:
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days
            else:
                record.validity = 90

    def _inverse_validity(self):
        for record in self:
            if record.date_deadline:
                record.date_availability = record.date_deadline - timedelta(days=record.validity or 90)

    # ───── ONCHANGE ─────

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ───── ACTION BUTTONS ─────

    def action_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled property cannot be sold.")
        self.state = 'sold'
        self.env['estate.property'].create({
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

    def action_view_accepted_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accepted Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id), ('status', '=', 'accepted')],
            'context': {'default_property_id': self.id},
            'target': 'current',
        }

    # ───── ORM METHODS ─────

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sold':
            for rec in self:
                if rec.state == 'cancelled':
                    raise UserError("Cancelled property cannot be sold.")
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError("Sold property cannot be deleted.")
        return super().unlink()

    def action_get_new_properties(self):
        new_properties = self.env['estate.property'].search([
            ('state', '=', 'new'),
            ('expected_price', '>', 0),
        ])
        names = ', '.join(new_properties.mapped('name'))
        raise UserError(f"New Properties: {names}")

    def action_browse_example(self):
        self.ensure_one()
        record = self.env['estate.property'].browse(self.id)
        raise UserError(f"Browsed Property: {record.name}")

    def action_count_new_properties(self):
        count = self.env['estate.property'].search_count([
            ('state', '=', 'new')
        ])
        raise UserError(f"Total New Properties: {count}")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['bedrooms'] = 3
        res['garden'] = True
        res['garden_area'] = 10
        return res

    # ───── SCHEDULED ACTION METHOD ─────

    @api.model
    def action_auto_cancel_expired_properties(self):
        today = fields.Date.today()
        expired_properties = self.search([
            ('state', '=', 'new'),
            ('date_deadline', '<', today),
        ])
        for prop in expired_properties:
            prop.state = 'cancelled'
            prop.message_post(
                body=f"Property automatically cancelled. "
                     f"Deadline {prop.date_deadline} has passed."
            )

    # ───── SERVER ACTION METHOD ─────

    def action_reset_to_new(self):
        for prop in self:
            if prop.state == 'sold':
                raise UserError(
                    f"Property '{prop.name}' is sold. Cannot reset to New."
                )
            prop.state = 'new'
            prop.message_post(
                body=f"Property reset to New by {self.env.user.name}."
            )
