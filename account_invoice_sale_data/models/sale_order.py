# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


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

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        portfolio_type = 'national'
        if self.partner_id.country_id and \
                self.partner_id.country_id.code != 'MX':
            portfolio_type = 'foreign'
        if self.priority == 'replenishment':
            portfolio_type = 'replacement'
        if self.priority == 'sample':
            portfolio_type = 'sample'
        invoice_vals['portfolio_type'] = portfolio_type
        return invoice_vals
