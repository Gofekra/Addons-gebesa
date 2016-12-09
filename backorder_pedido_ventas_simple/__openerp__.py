# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "barckorder pedido de ventas simples",
    "summary": "Reporte de Ventas por pedido Simple",
    "version": "9.0.1.0.0",
    "category": "Sales",
    "website": "https://odoo-community.org/",
    "author": "<jesus01x>",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base","sale",
    ],
    "data": [
        "views/sale_order.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}