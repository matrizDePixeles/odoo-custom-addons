from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campo que agregaste en la vista XML
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse') 

    # Campo computado que contendrá los IDs de los diarios permitidos
    allowed_journal_ids = fields.Many2many(
        'account.journal', 
        string='Allowed Journals', 
        compute='_compute_allowed_journal_ids',
        store=False,  # No es necesario almacenar este campo
    )

    @api.depends('warehouse_id')
    def _compute_allowed_journal_ids(self):
        """Calcula la lista de diarios permitidos para el dominio."""
        for move in self:
            if move.warehouse_id:
                # Obtenemos directamente los IDs de los diarios del almacén
                move.allowed_journal_ids = move.warehouse_id.pos_invoice_journal_ids
            else:
                # Si no hay almacén, permitir todos los diarios o ninguno, según tu lógica de negocio
                # Aquí asumimos que permitimos todos si no se ha seleccionado un almacén
                move.allowed_journal_ids = self.env['account.journal'].search([]) 
                # Si solo quieres que funcione si hay almacén, usa: move.allowed_journal_ids = False

