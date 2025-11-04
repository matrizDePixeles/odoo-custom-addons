from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_standard_price_incl_tax = fields.Monetary(
        string='Costo (Impuestos Incluidos)',
        compute='_compute_standard_price_incl_tax',
        inverse='_inverse_standard_price_incl_tax',
        currency_field='cost_currency_id',
        store=True
    )

    @api.depends('standard_price', 'supplier_taxes_id', 'taxes_id')
    def _compute_standard_price_incl_tax(self):
        for template in self:
            base_price = template.standard_price
            taxes = template.supplier_taxes_id or template.taxes_id
            if taxes:
                res = taxes.compute_all(
                    base_price,
                    currency=template.cost_currency_id,
                    quantity=1.0,
                    product=template,
                    partner=None
                )
                template.x_standard_price_incl_tax = res['total_included']
            else:
                template.x_standard_price_incl_tax = base_price

    def _inverse_standard_price_incl_tax(self):
        for template in self:
            price_incl = template.x_standard_price_incl_tax
            taxes = template.supplier_taxes_id or template.taxes_id
            if taxes:
                res = taxes.compute_all(
                    1.0,
                    currency=template.cost_currency_id,
                    quantity=1.0,
                    product=template,
                    partner=None
                )
                tax_factor = res['total_included']
                if tax_factor:
                    template.standard_price = price_incl / tax_factor
            else:
                template.standard_price = price_incl

