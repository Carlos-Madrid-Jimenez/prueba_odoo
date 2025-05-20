from odoo import http
from odoo.http import request

class IncidenciasController(http.Controller):
    @http.route("/incidencias/abiertos", auth="public")
    def incidencias_abiertos(self):
        tickets = request.env['incidencias.ticket'].sudo().search([])
        return request.render("incidencias.ticket_abiertos_template", {"tickets": tickets})