# -*- coding: utf-8 -*-
# from odoo import http


# class AlbaranCustom(http.Controller):
#     @http.route('/albaran_custom/albaran_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/albaran_custom/albaran_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('albaran_custom.listing', {
#             'root': '/albaran_custom/albaran_custom',
#             'objects': http.request.env['albaran_custom.albaran_custom'].search([]),
#         })

#     @http.route('/albaran_custom/albaran_custom/objects/<model("albaran_custom.albaran_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('albaran_custom.object', {
#             'object': obj
#         })
