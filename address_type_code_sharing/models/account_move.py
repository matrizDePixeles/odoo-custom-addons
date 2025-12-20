from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    associated_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Almacén Asociado',
        help='Selecciona el almacén para limitar los diarios disponibles.'
    )

    suitable_journal_ids = fields.Many2many(
        'account.journal',
        compute='_compute_suitable_journal_ids',
        string='Diarios Permitidos'
    )

    @api.depends('associated_warehouse_id')
    def _compute_suitable_journal_ids(self):
        AccountJournal = self.env['account.journal']
        empty = AccountJournal.browse([])
        for move in self:
            wh = move.associated_warehouse_id
            move.suitable_journal_ids = wh.pos_invoice_journal_ids if (wh and wh.pos_invoice_journal_ids) else empty

    @api.constrains('journal_id', 'associated_warehouse_id')
    def _check_journal_in_allowed(self):
        for move in self:
            if move.associated_warehouse_id:
                allowed = move.associated_warehouse_id.pos_invoice_journal_ids
                if move.journal_id and move.journal_id not in allowed:
                    raise ValidationError("El diario seleccionado no está permitido para el almacén asociado.")

    @api.constrains('associated_warehouse_id')
    def _check_warehouse_has_journals(self):
        for move in self:
            if move.associated_warehouse_id and not move.associated_warehouse_id.pos_invoice_journal_ids:
                raise ValidationError("El almacén seleccionado no tiene diarios configurados. Configura al menos uno en el almacén.")

    @api.constrains('associated_warehouse_id')
    def _check_warehouse_required(self):
        for move in self:
            if not move.associated_warehouse_id:
                raise ValidationError("Debe seleccionar un almacén asociado antes de guardar el documento.")

    @api.onchange('associated_warehouse_id')
    def _onchange_associated_warehouse_id(self):
        wh = self.associated_warehouse_id
        if not wh:
            return
        journals = wh.pos_invoice_journal_ids.filtered(lambda j: j.company_id == self.company_id)
        if journals:
            self.journal_id = journals[0].id
        else:
            self.journal_id = False
            return {
                'warning': {
                    'title': "Almacén sin diarios válidos",
                    'message': "El almacén no tiene diarios de venta para la compañía del documento.",
                    'type': 'notification'
                }
            }

