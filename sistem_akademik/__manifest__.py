{
    'name': 'Sistem Akademik',
    'version': '17.0.1.0.0',
    'summary': 'sistem akademik',
    'description': """  sistem akademik  """,
    'author': 'Hajril',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/akademik_tahun_view.xml',
        'views/akademik_prodi_view.xml',
        'views/mahasiswa_view.xml',
        'views/mahasiswa_s1_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
