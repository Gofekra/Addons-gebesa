# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _
from openerp.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    total_net_sale = fields.Float(
        string=_('Total Net Sale'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_freight = fields.Float(
        string=_('Freight Percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_freight = fields.Float(
        string=_('Total Freight'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_installation = fields.Float(
        string=_('Installation Percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_installation = fields.Float(
        string=_('Total Installation'),
        digits_compute=dp.get_precision('Account'),
    )

    profit_margin = fields.Float(
        string=_('Profit Margin'),
        digits_compute=dp.get_precision('Account'),
    )

    not_be_billed = fields.Boolean(
        string=_('Not be Billed'),
    )

    manufacture = fields.Selection(
        [('special', _('Special')),
            ('line', _('Line')),
            ('replenishment', _('Replenishment')),
            ('semi_special', _('Semi special'))],
        string=_("Manufacture"),

    )

    total_cost = fields.Float(
        string=_('Total Cost'),
        digits_compute=dp.get_precision('Account'),
    )

    executive = fields.Char(
        string=_('Executive'),
        size=100,
    )

    portfolio_type = fields.Selection(
        [('attested_copy', _(u'Attested copy')),
         ('national', _(u'National')),
         ('foreign', _(u'Foreign')),
         ('street_market', _(u'Street market')),
         ('replacement', _(u'Replacement')),
         ('bad_debt', _(u'Bad debt')),
         ('sample', _(u'Sample')),
         ('agreement', _(u'Agreement')),
         ('legal', _(u'Legal'))],
        string=_(u"Portfolio type"),
        states={'cancel': [('readonly', True)]},
        store=True,
        select=True,
        default='national',
    )

    itinerary = fields.Integer(
        'Itinerary',
        help='Itinerary number')
