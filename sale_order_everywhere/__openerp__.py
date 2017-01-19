# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Everywhere",
    "summary": "Sale Order Everywhere",
    "version": "9.0.1.0.0",
    "category": "Sale",
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
        "sale",
        "procurement",
        "stock",
        "mrp",
        "stock_picking_invoice",
    ],
    "data": [
        "views/sale_order.xml",
        "views/stock_move.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
