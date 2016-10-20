# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    geb_invoice_status = fields.Selection(
        [('no_invoice', _('No invoice')),
         ('partial_invoice', _('Partial invoice')),
         ('total_invoice', _(u'Total invoice'))],
        string=_("Invoice status"),
        store=True,
        select=True,
        default='no_invoice',
    )
