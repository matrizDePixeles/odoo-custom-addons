# models/pos_config.py
from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    # 1. Campo One2many para la relación inversa (Necesario para el inverse_name)
    stock_warehouse_ids = fields.One2many(
        'stock.warehouse', 
        'pos_config_id', 
        string='Almacenes Vinculados',
    )

    # 2. Redefinición del campo original SÓLO para añadir el inverse_name
    
    # Campo para Auto Validar Factura (ya existente)
    auto_check_invoice = fields.Boolean(
        string='Auto Validar Factura (POS)',
        # IMPORTANTE: Añadir la dependencia inversa
        inverse_name='stock_warehouse_ids.auto_check_invoice',
    )

    # --- ADICIÓN DEL CAMPO default_partner_id ---
    
    # Campo para Cliente Predeterminado (redefinido del campo original de pos.config)
    default_partner_id = fields.Many2one(
        'res.partner',
        string='Cliente Predeterminado',
        # El resto de atributos se heredan.
        # IMPORTANTE: Añadir la dependencia inversa
        inverse_name='stock_warehouse_ids.default_partner_id',
        # No es necesario poner store=True, ni compute/inverse, ya que se heredan del original.
    )

    # --- ADICIÓN DEL CAMPO l10n_pe_edi_send_invoice ---
    
    # Campo para Envío de Factura Electrónica (redefinido del campo original)
    l10n_pe_edi_send_invoice = fields.Boolean(
        # El string (etiqueta) se hereda, pero puedes redefinirlo si es necesario.
        # IMPORTANTE: Añadir la dependencia inversa
        inverse_name='stock_warehouse_ids.l10n_pe_edi_send_invoice',
    )
    # --- FIN DE ADICIÓN DEL CAMPO l10n_pe_edi_send_invoice ---
