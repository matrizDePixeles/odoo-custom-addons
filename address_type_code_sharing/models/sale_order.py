from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Se asume que el campo 'warehouse_id' ya existe en sale.order,
    # generalmente agregado por el módulo 'sale_stock' o similar.

    def _prepare_invoice(self):
        """
        Prepara los valores para la creación de una factura (account.move)
        desde un pedido de venta.
        """
        # Llama al método original para obtener los valores base
        res = super(SaleOrder, self)._prepare_invoice()
        
        # Lógica para inyectar el warehouse_id en el dict de creación de la factura
        # Se asume que 'associated_warehouse_id' es el campo Many2one a 'stock.warehouse' en account.move
        if self.warehouse_id:
            res.update({
                'associated_warehouse_id': self.warehouse_id.id,
            })
        
        return res
