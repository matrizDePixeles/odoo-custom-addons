from odoo import models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        res = super().create_invoices()

        orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        Move = self.env['account.move']

        for order in orders:
            invoices = Move.search([
                ('invoice_origin', '=', order.name),
                ('company_id', '=', order.company_id.id)
            ])
            wh = order.warehouse_id
            if not invoices:
                continue

            # Seleccionar un diario válido para la compañía del invoice
            journals = wh.pos_invoice_journal_ids.filtered(lambda j: j.company_id == order.company_id)
            journal_id = journals and journals[0].id or False

            # Escritura atómica para evitar violar el constrains
            for inv in invoices:
                vals = {'associated_warehouse_id': wh.id}
                # Solo tocar journal_id si difiere o si no es válido
                if not inv.journal_id or (journal_id and inv.journal_id.id != journal_id) or (journal_id is False):
                    vals['journal_id'] = journal_id
                inv.write(vals)

        return res

