# -*- coding: utf-8 -*-

{
    'name': 'Gestion des etiquettes des colis',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
Gestion des etiquettes des colis et des mouvements de stocks de ceux-ci
    """,
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': ['product', 'stock'],
    'data': ['view/is_etiquette_view.xml',
             'view/is_etiquette_sequence.xml',
             'wizard/is_generer_etiquette_view.xml',
             'wizard/is_changer_emplacement_view.xml',
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
