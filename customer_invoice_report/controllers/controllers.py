# -*- coding: utf-8 -*-
# from odoo import http


# class CustomerInvoiceReport(http.Controller):
#     @http.route('/customer_invoice_report/customer_invoice_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_invoice_report/customer_invoice_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_invoice_report.listing', {
#             'root': '/customer_invoice_report/customer_invoice_report',
#             'objects': http.request.env['customer_invoice_report.customer_invoice_report'].search([]),
#         })

#     @http.route('/customer_invoice_report/customer_invoice_report/objects/<model("customer_invoice_report.customer_invoice_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_invoice_report.object', {
#             'object': obj
#         })

