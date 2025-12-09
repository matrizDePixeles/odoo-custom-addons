# models/pos_config.py
from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    # 1. Campo One2many para la relación inversa
    stock_warehouse_ids = fields.One2many(
        'stock.warehouse', 
        'pos_config_id', 
        string='Almacenes Vinculados',
    )

    # 2. Redefinición del campo original SÓLO para añadir el inverse_name
    auto_check_invoice = fields.Boolean(
        string='Auto Validar Factura (POS)', # Puedes mantener tu string para override
        # El resto de atributos (default, help, etc.) se heredan del original.
        # IMPORTANTE: Añadir la dependencia inversa
        inverse_name='stock_warehouse_ids.auto_check_invoice',
    )
