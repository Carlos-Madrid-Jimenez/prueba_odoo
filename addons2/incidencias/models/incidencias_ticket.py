from odoo import api, fields, models

class Ticket(models.Model):
    _name = 'incidencias.ticket'
    _description = 'Ticket de incidencias'
    _inherit = ["mail.thread.cc", "mail.activity.mixin"]

    name = fields.Char(required=True, string="Nombre")
    descripcion = fields.Html(tracking=True)
    equipo_asociado_id = fields.Many2one("incidencias.equipo", string="Equipo")
    fecha_actualizacion = fields.Date(readonly=True)
    fecha_asignacion = fields.Date(readonly=True, default=lambda self: fields.Date.today())
    fecha_cierre = fields.Date(readonly=True)
    prioridad = fields.Selection(
        selection=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')],
        tracking=True
    )
    canal_id = fields.Many2one("incidencias.ticket.canal", string="Canal")
    categoria_id = fields.Many2one("incidencias.ticket.categoria", string="Categoría")
    estado = fields.Selection(
        selection=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')],
        default="abierto",
        tracking=True
    )

    def action_cerrar(self):
        for ticket in self:
            ticket.estado = "cerrado"
            ticket.fecha_cierre = fields.Date.today()
        return True

    def action_reabrir(self):
        for ticket in self:
            ticket.estado = "abierto"
            ticket.fecha_cierre = None
        return True

    @api.model
    def write(self, vals):
        for ticket in self:
            ticket.fecha_actualizacion = fields.Date.today()

        return super().create(vals)