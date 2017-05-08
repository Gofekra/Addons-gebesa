# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_cancel(self):
        for inv in self:
            if inv.date_invoice:
                if inv.state != 'draft':
                    if not self.env.user.has_group(
                            'res_users_cancel_invoice.group_cancel_pre_mon_inv'
                    ):
                        date_inv = self.date_invoice.split('-', 3)
                        today = str(fields.Date.today()).split('-', 3)
                        if date_inv[1] != today[1] or date_inv[0] != today[0]:
                            raise ValidationError(
                                _(u"You can only cancel an invoice within the same \
                                  month that was done the invoice.\nInstead \
                                  you should make full refund of the invoice"))
                    if not self.env.user.has_group(
                            'res_users_cancel_invoice.group_cancel_invoice'):
                        if inv.type in ('out_invoice', 'out_refund'):
                            raise ValidationError(
                                _(u"Only Administrator can cancel an invoice \
                                  or customer refund.\nPlease ask your system \
                                  administrator with an impression of this \
                                  invoice signed"))
                        if inv.type in ('in_invoice', 'in_refund'):
                            raise ValidationError(
                                _(u"Only Administrator can cancel an invoice \
                                  or return of raw material supplier.\nPlease\
                                  ask your system administrator with an \
                                  impression of this invoice signed"))
        super(AccountInvoice, self).action_cancel()
