# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock picking type",
    "summary": "Stock picking type",
    "version": "9.0.1.0.0",
    "category": "Personalized",
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
        "base", "stock", "mrp", "purchase", "sale"
    ],
    "data": [
        "views/stock_move_type.xml",
        "views/stock_move.xml",
        "views/stock_picking.xml",
        "views/type_adjustment.xml",
        "security/stock_move_type_security.xml",
        "security/ir.model.access.csv",
        "data/stock_move_type_data.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
