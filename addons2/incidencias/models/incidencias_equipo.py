from odoo import api, fields, models

class Equipo(models.Model):
    _name = 'incidencias.equipo'
    _description = 'Equipo'

    nombre = fields.Char(required=True)
    responsable = fields.Many2one("res.users")
    miembros = fields.Many2one("res.users")
    ticket_ids = fields.Many2one("incidencias.tickets")