# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import Counter, defaultdict

from odoo import _, api, fields, tools, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import OrderedSet
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockMoveLine(models.Model):
    #__name__ = 'albaran_custom_grouping.stock_move_line'
    _inherit = 'stock.move.line'

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = {}
        
        for move_line in self:
            # Clave personalizada basada SOLO en product_id para evitar duplicados artificiales
            line_key = str(move_line.product_id.id)

            # Si la clave no existe, la creamos
            if line_key not in aggregated_move_lines:
                aggregated_move_lines[line_key] = {
                    'name': move_line.product_id.display_name,
                    'description': False,  # Puedes personalizar esto
                    'qty_done': move_line.qty_done,
                    'product_uom': move_line.product_uom_id.name,
                    'product_uom_rec': move_line.product_uom_id,
                    'product': move_line.product_id,
                }
            else:
                # Sumamos la cantidad para el mismo producto
                aggregated_move_lines[line_key]['qty_done'] += move_line.qty_done

        return aggregated_move_lines
