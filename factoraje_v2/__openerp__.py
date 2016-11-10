# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Factoraje v2",
    "summary": "Factoraje v2",
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
        "base", "account",
        "gebesa_reconcile_advance",
        'account_account_global',
    ],
    "data": [
        "views/account_invoice.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
