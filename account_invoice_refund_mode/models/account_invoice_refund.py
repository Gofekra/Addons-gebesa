# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountInvoiceRefund(models.Model):
    _inherit = 'account.invoice.refund'

    @api.multi
    def compute_refund(self, mode='refund'):
        context = dict(self._context or {})
        context.update({'mode': mode})
        invoice = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        invoice.mode = mode
        res = super(AccountInvoiceRefund, self).compute_refund(invoice.mode)

        return res
