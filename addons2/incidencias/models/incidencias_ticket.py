from odoo import api, fields, models

class Ticket(models.Model):
    _name = 'incidencias.ticket'
    _description = 'Ticket de incidencias'

    nombre = fields.Char(required=True)
    descripcion = fields.Html()
    equipo_asociado = fields.Many2one("incidencias.equipo")
    fecha_actualizacion = fields.Date()
    fecha_asignacion = fields.Date()
    fecha_cierre = fields.Date()
    prioridad = fields.Selection(selection=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')])
    # canal_id
    categoria = fields.Many2one("incidencias.categoria")