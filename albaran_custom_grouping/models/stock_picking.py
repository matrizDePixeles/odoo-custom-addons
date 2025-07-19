# custom_addons_ezequiel/albaran_custom_grouping/models/stock_picking.py
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_report_delivery_landscape(self):
        # Este método se ejecutará cuando el usuario haga clic en "Albarán Formato Horizontal"
        # Odoo busca un método con el nombre de la acción de informe si el binding_type es 'report'
        # y no hay un modelo específico para el informe.

        # Prepara el contexto con tu bandera
        context = {
            'report_landscape_mode': True,
        }

        # Llama a la acción de impresión del informe, pasando el contexto
        return self.env.ref('albaran_custom_grouping.action_report_delivery_landscape').report_action(self, data=None, config=False, context=context)
