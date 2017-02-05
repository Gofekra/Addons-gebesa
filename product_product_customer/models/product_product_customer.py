# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductProductCustomer(models.Model):
    _name = 'product.product.customer'
    rec_name = 'client_code'

    customer_code = fields.Char(
        string='Customer Product Code',
        size=64,
    )
    customer_description = fields.Char(
        string='Customer Product Description',
        translate=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    qty = fields.Integer(
        'Quantity',
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_customer_ids = fields.One2many(
        'product.product.customer',
        'product_id',
        string='Customer product',
    )
