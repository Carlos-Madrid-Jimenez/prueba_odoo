from odoo import api, fields, models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property type'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property", "offer_ids", string="offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'The name must be unique')
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([
                ('property_type_id', '=', record.id)
            ])