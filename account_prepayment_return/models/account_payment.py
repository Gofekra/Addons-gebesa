# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    prepayment_type = fields.Selection(
        selection_add=[('advance_refund', _('Advance Refund'))],
        default='normal',
    )

    advance_refund_id = fields.Many2one(
        'account.payment',
        string=_('Advance to Return'),
    )

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        for rec in self:
            if rec.advance_refund_id and \
               rec.prepayment_type == 'advance_refund':
                if rec.advance_refund_id.payment_date > rec.payment_date:
                    raise UserError(_('Error!'
                                      '\nThe date of the advance may'
                                      'not exceed the date of the return.'))
                adv_amount = rec.advance_refund_id.pending_amount
                ret_amount = rec.amount
                total = adv_amount - ret_amount
                if total == 0.0:
                    rec.state = 'reconciled'
                    rec.advance_refund_id.state = 'reconciled'
                    rec.advance_refund_id.pending_amount = 0.0

            return res
