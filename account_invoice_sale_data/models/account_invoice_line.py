# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _
from openerp.addons import decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    margin_justification = fields.Char(
        string=_('P. M. Justification'),
        size=100,
        help=_('Low-margin justification for the invoice'),
    )

    net_sale = fields.Float(
        string=_('Net Sales'),
        digits_compute=dp.get_precision('Account'),
    )

    freight_amount = fields.Float(
        string=_('Freight Amount'),
        digits_compute=dp.get_precision('Account'),
    )

    installation_amount = fields.Float(
        string=_('Installation Amount'),
        digits_compute=dp.get_precision('Account'),
    )

    standard_cost = fields.Float(
        string=_('Standard Cost'),
        digits_compute=dp.get_precision('Account'),
    )

    total_cost = fields.Float(
        string=_('Total Cost'),
        digits_compute=dp.get_precision('Account'),
    )

    profit_margin = fields.Float(
        string=_('Profit Margin'),
        digits_compute=dp.get_precision('Account'),
    )
