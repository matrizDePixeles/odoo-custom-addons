from odoo import fields, models

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    picking_partner_id = fields.Many2one(
        'res.partner',
        string='Contacto',
        related='picking_id.partner_id',
        readonly=True,
        store=True 
    )
    