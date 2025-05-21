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
    equipo_asociado_id = fields.Many2one("incidencias.equipo", string="Equipo", required=True)
    persona_asignada_id = fields.Many2one("res.users", string="Persona asociada")
    aula_id = fields.Many2one("incidencias.aula", string="Aula")
    plano_aula = fields.Image(related="aula_id.plano", string="Plano")
    fecha_actualizacion = fields.Datetime(readonly=True)
    fecha_asignacion = fields.Datetime(readonly=True, default=lambda self: fields.Datetime.now(), tracking=True)
    fecha_cierre = fields.Datetime(readonly=True)
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

    def to_json(self):
        return {'codigo': self.codigo, 'nombre': self.name}

    @api.model
    def _group_estados(self, estados, domain, order):
        return ['nuevo', 'en_progreso', 'en_espera', 'completado', 'cancelado', 'invalido']

    @api.model
    def create(self, vals):
        record = super().create(vals)

        if vals.get("equipo_asociado_id"):
            nombre_equipo = record.equipo_asociado_id.name
            palabras = nombre_equipo.split()
            prefijo = ''.join([palabra[0].upper() for palabra in palabras if palabra])

            record.write({'codigo': f'{prefijo}-{record.id}'})

        template_correo = self.env.ref('incidencias.ticket_mail_template')

        if record.equipo_asociado_id:
            miembros_equipo = self.env['res.users'].search([
                ('id', 'in', record.equipo_asociado_id.miembros.ids)
            ])

            for miembro in miembros_equipo:
                template_correo.with_context(email_to=miembro.email).send_mail(
                    record.id, force_send=True, email_values={'email_to': miembro.email}
                )

        return record

    def write(self, vals):
        vals["fecha_actualizacion"] = fields.Datetime.now()

        if vals.get("estado"):
            if vals["estado"] == "completado":
                vals["fecha_cierre"] = fields.Datetime.now()

                template_correo = self.env.ref('incidencias.ticket_cerrado_mail_template')

                if self.equipo_asociado_id:
                    miembros_equipo = self.env['res.users'].search([
                        ('id', 'in', self.equipo_asociado_id.miembros.ids)
                    ])

                    for miembro in miembros_equipo:
                        template_correo.with_context(email_to=miembro.email).send_mail(
                            self.id, force_send=True, email_values={'email_to': miembro.email}
                        )


        if vals.get("persona_asignada_id"):
            if self.estado == "nuevo":
                vals["estado"] = "en_progreso"

        return super(Ticket, self).write(vals)

    def asignarme_a_mi(self):
        for ticket in self:
            ticket.persona_asignada_id = self.env.user.id
