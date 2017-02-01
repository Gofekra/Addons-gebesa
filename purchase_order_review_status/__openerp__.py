# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Review Status",
    "summary": "Shows the review status of the purchase order",
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
        "stock_tree_views",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "wizard/purchase_order_lines_validate.xml",
    ],
    "demo": [

    ],
    "qweb": [

    ]
}
