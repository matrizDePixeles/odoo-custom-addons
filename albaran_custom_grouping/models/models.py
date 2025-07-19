# -*- coding: utf-8 -*-
from odoo import models, fields, api

#class StockMoveLine(models.Model):
#    _inherit = 'stock.move.line'
#
#    def _get_aggregated_product_quantities(self, **kwargs):
#        aggreta = super(StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)

# class albaran_custom(models.Model):
#     _name = 'albaran_custom.albaran_custom'
#     _description = 'albaran_custom.albaran_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
