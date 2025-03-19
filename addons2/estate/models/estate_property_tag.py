from odoo import api, fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tag'

    name = fields.Char(required=True)