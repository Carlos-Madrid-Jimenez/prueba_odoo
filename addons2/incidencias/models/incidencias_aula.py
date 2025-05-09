from odoo import fields, models

class Ticket(models.Model):
    _name = 'incidencias.aula'
    _description = 'Aula'

    name = fields.Char(required=True, string="Nombre")
    # estado = fields.Many2one("incidencias.aula.estado")
    plano = fields.Image(string="Plano")
    # items = fields.Many2many("incidencias.aula.item")