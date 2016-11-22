# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Shipment",
    "summary": "MRP Shipment",
    "version": "9.0.1.0.0",
    "category": "MRP",
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
        "base", "mrp", "sale",
        "stock_warehouse_analytic_id",
    ],
    "data": [
        "views/mrp_shipment.xml",
        "views/sale_order.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
