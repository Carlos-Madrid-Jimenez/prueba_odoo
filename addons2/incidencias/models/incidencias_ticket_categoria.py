from odoo import fields, models

class TicketCategoria(models.Model):
    _name = 'incidencias.ticket.categoria'
    _description = 'Categoría'

    name = fields.Char(required=True, string="Nombre")