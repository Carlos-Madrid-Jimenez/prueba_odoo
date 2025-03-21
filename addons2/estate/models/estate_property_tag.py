from odoo import api, fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()