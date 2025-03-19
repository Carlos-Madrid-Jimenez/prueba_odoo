from odoo import api, fields, models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property type'

    name = fields.Char(required=True)