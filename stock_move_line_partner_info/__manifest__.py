# -*- coding: utf-8 -*-
{
    'name': "Campo contacto para movimiento de productos",
    'summary': "Agrega el campo contacto de transferencias para que aparezca tambien en movimiento de productos.",
    'version': '14.0.0.0',
    'author': 'Ezequiel Manaure',
    'depends': ['base', 'stock'],
    'data': [
        'views/view_move_line_form.xml',
        'views/view_move_line_tree.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}