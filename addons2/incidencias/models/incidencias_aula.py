from odoo import fields, models

class Ticket(models.Model):
    _name = 'incidencias.aula'
    _description = 'Aula'

    name = fields.Char(required=True, string="Nombre")
    # estado = fields.Many2one("incidencias.aula.estado")
    plano = fields.Image(string="Plano")
    ticket_ids = fields.One2many("incidencias.ticket", "aula_id", string="Tickets asociados")
    # items = fields.Many2many("incidencias.aula.item")