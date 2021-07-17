# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

{
    'name': 'Stock Inventory Valuation Report On Particular Date',
    'version': '14.0.1.0',
    'category': 'stock',
    'summary': 'Past Date Stock With Valuation Report in XLS/PDF',
    'description': """
Stock Valuation Report on Date,
----------------------------------
""",
    'author': 'TidyWay',
    'website': 'http://www.tidyway.in',
    'depends': ['stock_account'],
    'data': [
        'security/stock_valuation_security.xml',
        'security/ir.model.access.csv',
        'wizard/stock_valuation.xml',
        'views/stock_valuation_menu.xml',
        'views/stock_valuation_template.xml'
    ],
    'price': 80,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'images': ['images/valuation.jpg'],
    'live_test_url' : 'https://youtu.be/T37XNAYv6I8'
}
