from odoo import api, fields, models, Command

class Property(models.Model):
    _inherit = 'estate.property'
    _description = 'Estate property'

    def action_sold(self):
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.offer_ids.partner_id.id,
                'move_type': "out_invoice",
                'invoice_line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": record.selling_price * 0.06,
                        "price_unit": 0,
                    }),
                    Command.create({
                        "name": record.name,
                        "quantity": record.selling_price + 100.00,
                        "price_unit": 0,
                    })
                ]
            })

        return super().action_sold()