# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    rate = fields.Float(
        string=_('Type of change'),
        help=_('Rate used in the date of invoice'),
    )

    @api.multi
    def action_move_create(self):
        currency_obj = self.env['res.currency']
        res = super(AccountInvoice, self).action_move_create()

        for inv in self:
            currency_id = inv.currency_id.id
            currency = currency_obj.browse(currency_id)
            rate = currency.with_context(
                date=inv.date_invoice)._get_current_rate(
                inv.date_invoice, None)
            inv.rate = rate[currency_id]

        return res
