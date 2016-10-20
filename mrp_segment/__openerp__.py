# -*- coding: utf-8 -*-
# © <2016> <César Barrón>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Segment",
    "summary": "Performs a Segment",
    "version": "9.0.1.0.0",
    "category": "MRP",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro>, Odoo Community Association (OCA)",
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
        "mrp",
        "account",
        "stock_account",
    ],
    "data": [
        "views/mrp_segment_view.xml",
        "views/sale_order_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
