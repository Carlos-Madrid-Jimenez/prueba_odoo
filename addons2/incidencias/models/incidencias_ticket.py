from odoo import api, fields, models

class Ticket(models.Model):
    _name = 'incidencias.ticket'
    _description = 'Ticket de incidencias'
    _inherit = ["mail.thread.cc", "mail.activity.mixin"]

    name = fields.Char(required=True, string="Nombre")
    sequence = fields.Integer(
        index=True,
        default=10,
    )
    codigo = fields.Char(readonly=True, string="Código")
    descripcion = fields.Html()
    equipo_asociado_id = fields.Many2one("incidencias.equipo", string="Equipo")
    persona_asignada_id = fields.Many2one("res.users", string="Persona asociada")
    fecha_actualizacion = fields.Date(readonly=True)
    fecha_asignacion = fields.Date(readonly=True, default=lambda self: fields.Date.today(), tracking=True)
    fecha_cierre = fields.Date(readonly=True)
    tiempo_dedicado = fields.Float()
    coste = fields.Float()
    prioridad = fields.Selection(
        selection=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')],
        tracking=True
    )
    canal_id = fields.Many2one("incidencias.ticket.canal", string="Canal")
    categoria_id = fields.Many2one("incidencias.ticket.categoria", string="Categoría")
    estado = fields.Selection(
        selection=[
            ('nuevo', 'Nuevo'), ('en_progreso', 'En progreso'), ('en_espera', 'En espera'),
            ('completado', 'Completado'), ('cancelado', 'Cancelado'),
            ('invalido', 'Inválido')
        ],
        group_expand="_group_estados",
        default="nuevo",
        tracking=True
    )

    @api.model
    def _group_estados(self, estados, domain, order):
        return ['nuevo', 'en_progreso', 'en_espera', 'completado', 'cancelado', 'invalido']

    @api.model
    def create(self, vals):
        record = super().create(vals)

        nombre_equipo = record.equipo_asociado_id.name
        palabras = nombre_equipo.split()
        prefijo = ''.join([palabra[0].upper() for palabra in palabras if palabra])

        record.write({'codigo': f'{prefijo}-{record.id}'})

        return record

    def write(self, vals):
        vals["fecha_actualizacion"] = fields.Date.today()

        return super(Ticket, self).write(vals)