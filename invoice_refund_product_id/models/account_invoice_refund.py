# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, netsvc
from openerp.addons import decimal_precision as dp
from openerp.exceptions import ValidationError


class AccountInvoiceRefund(models.Model):
    _inherit = 'account.invoice.refund'

    product_id = fields.Many2one(
        'product.product',
        string=_(u'Product'),
        ondelete='set null',
        select=True,
    )

    amount = fields.Float(
        _(u'Amount'),
        digits_compute=dp.get_precision('Account'),
    )

    @api.multi
    def compute_refund(self, mode='refund'):
        ctx = self._context.copy()

        invoice_obj = self.env['account.invoice']

        for ref in self:
            product_id = ref.product_id.id
            amount = ref.amount
            for inv in invoice_obj.browse(self._context.get('active_ids')):
                # journal_id = inv.journal_id.id
                if mode != 'refund':
                    if inv.amount_total != inv.residual:
                        raise ValidationError(_(u"Invalid operation, the bill \
                                              already has payments"))
                if amount > inv.residual:
                    raise ValidationError(_(u"Invalid operation, the balance \
                                          of the invoice is less than the \
                                          amount payable"))

        ctx.update({'product_id': product_id})
        ctx.update({'mode': mode})
        ctx.update({'amount': amount})

        res = super(AccountInvoiceRefund, self.with_context(
                    ctx)).compute_refund(mode)

        return res
