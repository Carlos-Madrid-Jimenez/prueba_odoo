from odoo import api, fields, models

class Categoria(models.Model):
    _name = 'incidencias.categoria'
    _description = 'Categoría'

    nombre = fields.Char(required=True)