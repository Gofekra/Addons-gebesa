# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Analytic Everywhere",
    "summary": "Add field analytic_account",
    "version": "9.0.1.0.0",
    "category": "Accounting",
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
        "base", "account", "stock", "purchase", "mrp"
    ],
    "data": [
        "views/account_invoice.xml",
        "views/mrp_production.xml",
        "views/purchase_order.xml",
        "views/stock_move.xml",
        "views/stock_picking.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
