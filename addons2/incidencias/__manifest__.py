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
        'data/ticket_mail_template.xml',
        'data/ticket_cerrado_mail_template.xml',
        'security/ir.model.access.csv',
        "security/security.xml",
        'views/incidencias_ticket_views.xml',
        'views/incidencias_ticket_categoria_views.xml',
        'views/incidencias_ticket_canal_views.xml',
        'views/incidencias_equipo_views.xml',
        'views/incidencias_aula_views.xml',
        'views/incidencias_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [],
    'license': 'LGPL-3',
    'application': True
}