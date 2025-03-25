{
    'name': "Estate",
    'version': '17.0.1.2',
    'depends': ['base'],
    'author': "Carlos Madrid Jiménez",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [],
    'license': 'LGPL-3',
    'application': True
}