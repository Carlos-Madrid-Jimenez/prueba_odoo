from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price must be strictly positive')
    ]

    @api.model
    def create(self, vals):
        for record in self:
            if self.env['estate.property'].browse(vals['property_id']).state == 'new':
                record.property_id.state = 'offer_received'

        return super().create(vals)

    @api.depends('property_id.offer_ids')
    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError('Only one offer can be accepted at a time')
            record.status = "accepted"
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                today = fields.Date.today()
                delta = record.date_deadline - today
                record.validity = delta.days