from odoo import api, fields, models
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
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
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
