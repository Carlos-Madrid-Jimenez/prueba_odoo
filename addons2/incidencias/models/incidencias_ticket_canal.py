from odoo import fields, models

class TicketCanal(models.Model):
    _name = "incidencias.ticket.canal"
    _description = "Canal"

    name = fields.Char(required=True, string="Nombre")
    active = fields.Boolean(default=True)