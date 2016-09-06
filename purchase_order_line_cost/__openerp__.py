# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Cost",
    "summary": "Purchase order line cost",
    "version": "9.0.1.0.0",
    "category": "Purchase",
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
        "base", "purchase",
    ],
    "data": [
        "views/purchase.xml"
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
