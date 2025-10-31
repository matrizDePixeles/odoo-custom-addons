{
    'name': 'Website Marquee References',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Personaliza el bloque de referencias del módulo Website con animación tipo marquesina.',
    'description': """
        Este módulo personaliza el bloque de referencias del constructor de sitios web de Odoo,
        agregando un efecto de desplazamiento horizontal infinito (marquesina) para logos o textos.
    """,
    'author': 'Ezequiel Manaure',
    'depends': ['website'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_marquee_references/static/src/css/custom.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
