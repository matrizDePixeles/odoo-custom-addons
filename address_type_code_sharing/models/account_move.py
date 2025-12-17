from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campo calculado y de solo lectura para el almacén asociado
    associated_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén Asociado',
        compute='_compute_associated_warehouse',
        store=True,  # Para que se guarde en la BD y se pueda consultar
        readonly=True,
    )

    @api.depends('journal_id', 'invoice_origin') # Añadir 'invoice_origin'
    def _compute_associated_warehouse(self):
        """
        Busca el almacén asociado con la siguiente prioridad:
        1. Almacén del Sale Order asociado (usando invoice_origin).
        2. Almacén asociado al diario (lógica existente).
        """
        for move in self:
            warehouse = False # Almacén que vamos a asignar

            # --- PRIORIDAD 1: Buscar por Sale Order asociado (invoice_origin) ---
            if move.invoice_origin:
                # Buscamos el pedido de venta (sale.order)
                sale_order = self.env['sale.order'].search([
                    ('name', '=', move.invoice_origin),
                    ('company_id', '=', move.company_id.id)
                ], limit=1)
                
                if sale_order and sale_order.warehouse_id:
                    warehouse = sale_order.warehouse_id.id
            
            # --- PRIORIDAD 2: Fallback a la lógica de búsqueda por Diario (journal_id) ---
            if not warehouse and move.journal_id:
                # Obtenemos todos los almacenes que tienen el journal_id actual en su pos_invoice_journal_ids
                warehouses = self.env['stock.warehouse'].search([
                    ('pos_invoice_journal_ids', 'in', move.journal_id.id)
                ], limit=1) # Limitamos a 1 para tomar el primero que coincida
                
                if warehouses:
                    warehouse = warehouses.id
            
            # Asignamos el valor final (o False si no se encontró nada)
            move.associated_warehouse_id = warehouse

    def action_post(self):
        self.ensure_one()
    
        company = self.company_id
        warehouse = self.associated_warehouse_id
        new_code = warehouse.l10n_pe_edi_address_type_code if warehouse else False
    
        if not company or not new_code:
            return super().action_post()
    
        # Bloqueo explícito
        self.env.cr.execute("SELECT id FROM res_company WHERE id = %s FOR UPDATE", [company.id])
    
        original_code = company.l10n_pe_edi_address_type_code
        try:
            company.l10n_pe_edi_address_type_code = new_code
            return super().action_post()
        finally:
            company.l10n_pe_edi_address_type_code = original_code

# Campo técnico para filtrar los diarios en la vista
    suitable_journal_ids = fields.Many2many(
        'account.journal', 
        compute='_compute_suitable_journal_ids'
    )

    @api.depends('associated_warehouse_id')
    def _compute_suitable_journal_ids(self):
        for move in self:
            if move.associated_warehouse_id and move.associated_warehouse_id.pos_invoice_journal_ids:
                # Si hay un almacén con diarios configurados, usamos esos
                move.suitable_journal_ids = move.associated_warehouse_id.pos_invoice_journal_ids.ids
            else:
                # Si no hay almacén, permitimos todos los diarios de venta de la compañía
                move.suitable_journal_ids = self.env['account.journal'].search([
                    ('type', '=', 'sale'),
                    ('company_id', '=', move.company_id.id)
                ]).ids
