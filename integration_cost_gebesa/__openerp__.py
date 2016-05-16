# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GEBESA integration cost",
    "summary": "Gebesa integration cost",
    "version": "9.0.1.0.0",
    "category": "Sale",
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
        "account_invoice_stock_picking_id",
        "integration_progress_fields",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/account_invoice.xml",
        "views/integration_cost_gebesa.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
