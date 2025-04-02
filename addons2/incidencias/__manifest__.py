{
    'name': "Incidencias",
    'version': '17.0.1.1',
    'depends': ["mail"],
    'author': "Carlos Madrid Jiménez",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/incidencias_ticket_views.xml',
        'views/incidencias_ticket_categoria_views.xml',
        'views/incidencias_equipo_views.xml',
        'views/incidencias_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [],
    'license': 'LGPL-3',
    'application': True
}