# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shiptment_status = fields.Selection(
        [('no_shipment', _('No shipment')),
         ('partial_shipment', _('Partial shipment')),
         ('total_shipment', _(u'Total shipment'))],
        string=_("Shiptment statu"),
        store=True,
        select=True,
        default='no_shipment',
    )
