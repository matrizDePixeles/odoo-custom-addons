# models/stock_warehouse.py
from odoo import models, fields

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    # Campo relacionado que accede al campo de la compañía a través de 'company_id'
    l10n_pe_edi_address_type_code = fields.Char(
        string="Código Tipo Dirección (Compañía)",
        # Accede al campo de la compañía a través de la relación 'company_id'
        related='company_id.l10n_pe_edi_address_type_code',
        readonly=True, # Por lo general, estos campos deben ser de solo lectura
    )

    pos_config_id = fields.Many2one(
        'pos.config',
        string='Punto de Venta Asociado',
        help='Enlaza este almacén con un punto de venta específico.',
    )
