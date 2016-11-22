# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Price List",
    "summary": "Report Price List",
    "version": "Product",
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
        "base", "product", "product_structure_gebesa",
    ],
    "data": [
        "views/product_template.xml",
        "report/report_price_list.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
