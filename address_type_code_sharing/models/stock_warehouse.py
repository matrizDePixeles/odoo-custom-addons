# models/stock_warehouse.py
from odoo import models, fields, api

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

    # Nuevo campo COMPUTADO y ALMACENABLE (Writable)
    pos_invoice_journal_ids = fields.Many2many(
        'account.journal', 
        string='Diarios de Facturación (POS)',
        compute='_compute_pos_invoice_journal_ids',
        inverse='_inverse_pos_invoice_journal_ids', # <-- FUNCIÓN INVERSA PARA ESCRITURA
        readonly=False, # <-- Debe ser editable en el formulario
        store=True,     # <-- Almacenamos el ID para evitar problemas al escribir en M2M
    )

    auto_check_invoice = fields.Boolean(
        string='Auto Validar Factura (POS)',
        compute='_compute_auto_check_invoice',
        inverse='_inverse_auto_check_invoice',
        readonly=False, # Permite la edición
        store=True,     # Almacenable para persistencia
        help='Si está marcado, las facturas generadas desde el POS asociado se validarán automáticamente.'
    )

    @api.depends('pos_config_id', 'pos_config_id.invoice_journal_ids') 
    def _compute_pos_invoice_journal_ids(self):
        """Obtiene los diarios del POS enlazado."""
        for warehouse in self:
            if warehouse.pos_config_id:
                warehouse.pos_invoice_journal_ids = warehouse.pos_config_id.invoice_journal_ids
            else:
                warehouse.pos_invoice_journal_ids = [(5, 0, 0)]

    def _inverse_pos_invoice_journal_ids(self):
        """
        Función inversa: Cuando el campo pos_invoice_journal_ids se edita en el almacén, 
        se actualiza el campo original (invoice_journal_ids) en el registro de pos.config.
        """
        for warehouse in self:
            # Solo actualizamos si hay un POS configurado
            if warehouse.pos_config_id:
                # Escribimos los nuevos IDs de diarios en el registro de pos.config
                warehouse.pos_config_id.invoice_journal_ids = warehouse.pos_invoice_journal_ids

    # --- NUEVAS FUNCIONES PARA auto_check_invoice ---

    @api.depends('pos_config_id', 'pos_config_id.auto_check_invoice') # <-- AÑADIDO: Dependencia del campo original
    def _compute_auto_check_invoice(self):
        """Obtiene el valor de auto_check_invoice del POS enlazado."""
        for warehouse in self:
            # Si hay un POS configurado, toma su valor; si no, es False.
            warehouse.auto_check_invoice = warehouse.pos_config_id.auto_check_invoice if warehouse.pos_config_id else False

    def _inverse_auto_check_invoice(self):
        """
        Función inversa: Cuando se edita auto_check_invoice en el almacén, 
        se actualiza el campo original en el registro de pos.config.
        """
        for warehouse in self:
            if warehouse.pos_config_id:
                # Escribimos el nuevo valor en el registro de pos.config
                warehouse.pos_config_id.auto_check_invoice = warehouse.auto_check_invoice
