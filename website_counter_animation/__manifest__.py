{
    'name': 'Website Counter Animation',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Personaliza el bloque de numeros del módulo Website con animación de incremento.',
    'description': """
        Este módulo personaliza el bloque de números del constructor de sitios web de Odoo,
        agregando un efecto de crecimiento gradual del número.
    """,
    'author': 'Ezequiel Manaure',
    'depends': ['website'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_counter_animation/static/src/js/counter_animation.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
