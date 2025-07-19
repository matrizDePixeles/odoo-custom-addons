# -*- coding: utf-8 -*-
{
    'name': "Albaran Custom Grouping",
    'summary': "Agrega los campos de vendedor y plazo de pago al Albaran.",
    'version': '1.0',
    'author': 'Ezequiel Manaure',
    'depends': ['base', 'stock', 'facturaclic_pe_guide'],
    'data': [
        'report/report_picking.xml',
        'report/report_deliveryslip.xml',
        'report/paperformat.xml',
        'report/report_action.xml',
        'report/report_action_button.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}