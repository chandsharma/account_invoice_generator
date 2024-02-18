from odoo import http
from odoo.http import request
import random
import datetime

class InvoiceGenerator(http.Controller):

    @http.route('/generate_invoices/<int:count>', type='http', auth="user")
    def generate_invoices(self, count,**kw):
        env = request.env
        partner_ids = env['res.partner'].search([]).ids
        product_ids = env['product.product'].search([]).ids

        def random_date(start, end):
            return start + datetime.timedelta(
                seconds=random.randint(0, int((end - start).total_seconds())),
            )

        for _ in range(count):  # Adjust the range for the number of invoices
            partner_id = random.choice(partner_ids)
            product_id = random.choice(product_ids)
            invoice_date = random_date(datetime.date(2023, 9, 1), datetime.date.today())

            invoice = request.env['account.move'].sudo().create({
                'partner_id': partner_id,
                'journal_id': 1,
                'move_type': 'out_invoice',
                'invoice_date': invoice_date,
                'invoice_line_ids': [(0, 0, {
                    'product_id': product_id,
                    'quantity': random.randint(1, 10),
                    'name': env['product.product'].browse(product_id).name,
                    'price_unit': env['product.product'].browse(product_id).list_price,
                })],
            })
        invoice_ids = env['account.move'].search([('state','=','draft')])
        for invoice_id in invoice_ids:
            if invoice_id.invoice_line_ids:
                invoice_id.action_post()

        return "Invoices Generated Successfully"
