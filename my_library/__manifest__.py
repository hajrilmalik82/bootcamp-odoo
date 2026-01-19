{
    'name': "Library Management",
    'summary': "Manage Books, Authors, and Categories",
    'description': """
        Library Management System for managing:
        - Books
        - Authors
        - Categories
    """,
    'author': "Hajril",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '17.0.1.0.0',
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_author.xml',
        'views/library_category.xml',
        'views/res_partner.xml',
        'views/library_organization.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}