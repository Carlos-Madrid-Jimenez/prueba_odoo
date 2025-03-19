import logging
from datetime import timedelta
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

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
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    @api.depends('create_date', 'validity', 'date_deadline')
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
                _logger.info("Calculando validity: date_deadline = %s, today = %s, delta.days = %d",
                             record.date_deadline, today, delta.days)
                record.validity = delta.days