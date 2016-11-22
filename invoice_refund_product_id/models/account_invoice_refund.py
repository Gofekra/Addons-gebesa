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
        account_m_line = self.env['account.move.line']
        wf_service = netsvc.LocalService('workflow')

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
        refund_id = res['domain'][1][2][0]

        wf_service.trg_validate(self._uid, 'account.invoice', refund_id,
                                'invoice_open', self._cr)

        for form in self:
            for invoice in invoice_obj.browse(self._context.get('active_ids')):
                if mode == 'refund':
                    to_reconcile_ids = {}
                    refund = invoice_obj.browse(refund_id)
                    for tmp_line in refund.move_id.line_ids:
                        if tmp_line.account_id.id == inv.account_id.id:
                            to_reconcile_ids[tmp_line.account_id.id] = [
                                tmp_line.id]
                    for account in to_reconcile_ids:
                        invoice.register_payment(account_m_line.browse(
                            to_reconcile_ids[account]))
        return res
