from odoo import api, fields, models

class Equipo(models.Model):
    _name = 'incidencias.equipo'
    _description = 'Equipo'

    name = fields.Char(required=True, string="Nombre")
    responsable = fields.Many2one("res.users")
    miembros = fields.Many2one("res.users")
    ticket_ids = fields.One2many("incidencias.ticket", "equipo_asociado_id")