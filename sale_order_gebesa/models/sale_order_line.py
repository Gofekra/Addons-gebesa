# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _
from openerp.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_justification = fields.Char(
        string=_(u'P. M. justification'),
        size=100,
        help=_(u'low-margin justification for the sales order'),
    )

    net_sale = fields.Float(
        string=_(u'Net sales'),
        digits_compute=dp.get_precision('Account'),
    )

    freight_amount = fields.Float(
        string=_(u'Freight amount'),
        digits_compute=dp.get_precision('Account'),
    )

    installation_amount = fields.Float(
        string=_(u'installation amount'),
        digits_compute=dp.get_precision('Account'),
    )

    standard_cost = fields.Float(
        string=_(u'Standard cost'),
        digits_compute=dp.get_precision('Account'),
    )

    profit_margin = fields.Float(
        string=_(u'Profit margin'),
        digits_compute=dp.get_precision('Account'),
    )

    fulfilled = fields.Float(
        string=_(u'Fulfilled'),
        digits_compute=dp.get_precision('Account'),
        help=_(u'Fulfilled'),
    )

    invoiced = fields.Float(
        string=_(u'Invoiced'),
        digits_compute=dp.get_precision('Account'),
        help=_(u'Invoiced')
    )
