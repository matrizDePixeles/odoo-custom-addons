{
    'name': 'Address Type Code Sharing',
    'version': '1.0',
    'category': '',
    'summary': """
""",
    'description': """
Este módulo personaliza la configuración de almacén agregando nuevos campos: address_type_code y diarios permitidos. Se agrega también un campo llamado almacén asociado que es obligatorio para la generación de la factura o boleta. Este campo se consulta para dos fines: 

1. Determinar el address_type_code que debe mostrarse en la factura o boleta según el almacén asociado.
2. Filtrar los diarios e impedir que se utilice un diario que no pertenezca al almacén asociado.
    """,
    'author': 'Ezequiel Manaure',
    'depends': ['account', 'sale_management','stock', 'point_of_sale', 'facturaclic_pe_cpe','facturaclic_pe_pos', 'facturaclic_pe_server'],
    'data': [
        'views/view_warehouse_inherit_move_field.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
