# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _
from openerp.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    ns_internal_id = fields.Char(
        string=_('Internal ID in Netsuite'),
    )

    total_nste = fields.Float(
        string=_('Total Netsuite'),
        digits_compute=dp.get_precision('Account'),
        help=_('Total order in NetSuite'),
    )

    date_netsuite = fields.Char(
        string=_('NetSuite capture date'),
        select=True,
    )

    ok_etl = fields.Boolean(
        string=_('OK ETL'),
        select=False,
    )
