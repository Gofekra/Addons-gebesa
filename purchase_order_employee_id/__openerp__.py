# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Employee",
    "summary": "Add field for Employee in Purchase Order",
    "version": "9.0.1.0.0",
    "category": "Purchase",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "purchase",
        "hr",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
