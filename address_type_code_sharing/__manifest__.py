{
    'name': 'Address Type Code Sharing',
    'version': '1.0',
    'category': '',
    'summary': 'Comparte el address type code de la empresa sus almacenes.',
    'description': """
        Este modulo <field name="l10n_pe_edi_address_type_code"/>.
    """,
    'author': 'Ezequiel Manaure',
    'depends': ['account','stock', 'point_of_sale', 'facturaclic_pe_pos', 'facturaclic_pe_server'],
    'data': [
        'views/view_warehouse_inherit_move_field.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
