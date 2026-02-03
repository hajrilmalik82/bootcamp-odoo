{
    'name': 'Dosen Akademik',
    'version': '1.0',
    'description': """Modul Keren Dosen""",
    'author': 'Hajril',
    'depends': ['base', 'hr', 'sistem_akademik'],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'akademik_dosen/static/src/css/dosen_style.css',
        ],
    },
    'installable': True,
    'application': False,
}
