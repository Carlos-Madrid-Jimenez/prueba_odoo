from odoo import http
from odoo.http import request

import json

class IncidenciasController(http.Controller):
    @http.route("/incidencias/abiertos", auth="public", type="http")
    def incidencias_abiertos(self):
        tickets = request.env['incidencias.ticket'].sudo().search([])
        tickets_data = []

        for t in tickets:
            tickets_data.append(t.to_json())

        return request.make_json_response(tickets_data)
        # return request.render("incidencias.ticket_abiertos_template", {"tickets": tickets})