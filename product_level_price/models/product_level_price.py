# -*- coding: utf-8 -*-
# © 2017 Aldo Nerio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductLevelPrice(models.Model):
    _name = 'product.level.price'
    _description = 'Product Price Level'
    _order = 'product_id asc'
    _rec_name = 'product_id'

    price_dis_a = fields.Float(
        string=_('Price Dis 00:'),
        help=_('Price 00')
    )

    price_dis_b = fields.Float(
        string=_('Price Dis 00-01:'),
        help=_('Price 00.01')
    )

    price_dis_c = fields.Float(
        string=_('Price Dis 01:'),
        help=_('Price 01')
    )

    price_dis_d = fields.Float(
        string=_('Price Dis 02:'),
        help=_('Price 02')
    )

    price_dis_e = fields.Float(
        string=_('Price Dis 03:'),
        help=_('Price 03')
    )

    price_dis_f = fields.Float(
        string=_('Price Dis 04:'),
        help=_('Price 04')
    )

    price_dis_g = fields.Float(
        string=_('Price Dis 05:'),
        help=_('Price 05')
    )

    price_dis_h = fields.Float(
        string=_('Price Dis 06:'),
        help=_('Price 06')
    )

    price_dis_i = fields.Float(
        string=_('Price Dis 07:'),
        help=_('Price 07')
    )

    base_price = fields.Float(
        string=_('Base Price:'),
        help=_('Base.Price')
    )

    price_dis_may = fields.Float(
        string=_('Base Dis-May 03:'),
        help=_('Base Price 03')
    )

    price_may_a = fields.Float(
        string=_('Price May 00:'),
        help=_('Price May')
    )

    price_may_b = fields.Float(
        string=_('Price May 01:'),
        help=_('Price May')
    )

    price_may_c = fields.Float(
        string=_('Price May 02:'),
        help=_('Price May')
    )

    price_may_d = fields.Float(
        string=_('Price May 03:'),
        help=_('Price May')
    )

    price_may_e = fields.Float(
        string=_('Price May 04:'),
        help=_('Price May')
    )

    price_may_f = fields.Float(
        string=_('Price May 05:'),
        help=_('Price May')
    )

    price_may_g = fields.Float(
        string=_('Price May 06:'),
        help=_('Price May')
    )

    price_may_h = fields.Float(
        string=_('Price May 07:'),
        help=_('Price May')
    )

    standard_cost = fields.Float(
        string=_(u'Cost Std:'),
        related='product_id.standard_price',
        readonly=True, 
    )

    product_id = fields.Many2one(
        'product.product',
        string=_('Product:'),
        help=_('Product'),
        required=True,
    )

    mu_dist_may_id = fields.Many2one(
        'product.product.mu',
        string=_('M.U.Dist - May:'),
        help=_('Product'),
        required=True,
    )

    description = fields.Selection(
        [('metal', _('Metal-Madera')),
         ('silleria', _('Silleria-Cyber'))],
        string=_('Description:'),
        select=True,
        default='metal',
        required=True,
    )
