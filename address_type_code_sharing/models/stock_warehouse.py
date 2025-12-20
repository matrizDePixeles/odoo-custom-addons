# models/stock_warehouse.py
from odoo import models, fields, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    l10n_pe_edi_address_type_code = fields.Char(
        string="Address Type Code"
    )

    pos_invoice_journal_ids = fields.Many2many(
        'account.journal', 
        string='Diarios'
    )

    default_partner_id = fields.Many2one(
        'res.partner',
        string='Cliente Habitual',
    )
