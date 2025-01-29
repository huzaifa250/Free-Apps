# -*- coding: utf-8 -*-
# from odoo import http


# class TestDev(http.Controller):
#     @http.route('/test_dev/test_dev', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_dev/test_dev/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_dev.listing', {
#             'root': '/test_dev/test_dev',
#             'objects': http.request.env['test_dev.test_dev'].search([]),
#         })

#     @http.route('/test_dev/test_dev/objects/<model("test_dev.test_dev"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_dev.object', {
#             'object': obj
#         })

