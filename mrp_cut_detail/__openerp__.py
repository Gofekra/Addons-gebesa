# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Cut Detail",
    "summary": "Add cut detail for Bill of Materials",
    "version": "9.0.1.0.0",
    "category": "MPR",
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
        "product",
        "mrp",
        "mrp_product_color",
        "mrp_product_caliber",
    ],
    "data": [
        "views/mrp_view.xml",
        "views/mrp_bom_line_view.xml",
        "views/mrp_bom_line_detail_view.xml",
        "views/mrp_bom_line_detail_operation.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
