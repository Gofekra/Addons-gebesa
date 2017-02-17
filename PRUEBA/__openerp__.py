{
    "name": "Prueba",
    "summary": "prueba",
    "version": "9.0.1.0.0",
    "category": "Accounting",
    "website": "https://odoo-community.org/",
    "author": "<Aldo>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "account"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/prueba.xml"
    ],
    "demo": [
    ],
    "qweb": [
    ]
}