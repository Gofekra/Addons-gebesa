# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock batch picking personalized",
    "summary": "Stock batch picking",
    "version": "9.0.1.0.0",
    "category": "inventory",
    "website": "https://odoo-community.org/",
    "author": "<Samuel Barron>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "stock",
        "stock_batch_picking"
    ],
    "data": [
        "views/stock_batch_picking.xml"
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
