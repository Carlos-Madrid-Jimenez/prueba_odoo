from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
import dateutil

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + dateutil.relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price", readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    total_area = fields.Integer(compute="_compute_total_area", readonly=True)
    active = fields.Boolean(default=False)
    state = fields.Selection(
        copy=False,
        required=True,
        default='new',
        string='State',
        selection=[('new', 'New'), ("offer_received", 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    buyer = fields.Many2one('res.partner', copy=False)
    salesman = fields.Many2one('res.users', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive')
    ]

    def action_sold(self):
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise UserError('Sold properties cannot be canceled')
        return True

    def action_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise UserError('Canceled properties cannot be sold')
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError(f'The selling price must not be below 90% of the expected price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
