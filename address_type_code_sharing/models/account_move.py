from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campo calculado y de solo lectura para el almacén asociado
    associated_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén Asociado',
        compute='_compute_warehouse_from_journal',
        store=True,  # Para que se guarde en la BD y se pueda consultar
        readonly=True,
    )

    @api.depends('journal_id')
    def _compute_warehouse_from_journal(self):
        """
        Busca el almacén asociado al diario de la factura
        a través de los campos pos_invoice_journal_ids en stock.warehouse.
        """
        # Obtenemos todos los almacenes que tienen el journal_id actual en su pos_invoice_journal_ids
        # Usamos self.env['stock.warehouse'].search para buscar en el modelo stock.warehouse
        
        # Preparamos una lista de IDs de diarios de las facturas actuales
        journal_ids = self.mapped('journal_id').ids
        
        if not journal_ids:
            for move in self:
                move.associated_warehouse_id = False
            return

        # Buscamos todos los almacenes que contengan alguno de los diarios de las facturas
        # {'pos_invoice_journal_ids': [('in', journal_ids)]} es una búsqueda relacional
        warehouses = self.env['stock.warehouse'].search([
            ('pos_invoice_journal_ids', 'in', journal_ids)
        ])

        # Creamos un mapeo rápido de {journal_id: warehouse_id}
        # Solo asignamos el primer almacén encontrado para cada diario (como pediste: "hallar la primera coincidencia")
        journal_to_warehouse = {}
        for warehouse in warehouses:
            for journal in warehouse.pos_invoice_journal_ids:
                if journal.id in journal_ids and journal.id not in journal_to_warehouse:
                    journal_to_warehouse[journal.id] = warehouse.id
                    
        # Asignamos el valor a cada factura
        for move in self:
            if move.journal_id.id in journal_to_warehouse:
                move.associated_warehouse_id = journal_to_warehouse[move.journal_id.id]
            else:
                move.associated_warehouse_id = False

    def action_post(self):
        if not self or not self[0].associated_warehouse_id:
            return super(AccountMove, self).action_post()

        company = self[0].company_id
        warehouse = self[0].associated_warehouse_id
        
        if not company or not warehouse:
            return super(AccountMove, self).action_post()

        # 1. Guardar copia
        original_address_code = company.l10n_pe_edi_address_type_code
        new_address_code = warehouse.l10n_pe_edi_address_type_code
        
        # 2. Sustituir valor (Pre-confirmación)
        company.l10n_pe_edi_address_type_code = new_address_code

        # 3. Ejecutar el proceso estándar
        res = super(AccountMove, self).action_post()
        
        # 4. Restaurar valor (Post-confirmación)
        company.l10n_pe_edi_address_type_code = original_address_code
            
        return res
