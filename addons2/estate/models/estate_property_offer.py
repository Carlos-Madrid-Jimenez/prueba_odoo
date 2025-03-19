from odoo import api, fields, models

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)