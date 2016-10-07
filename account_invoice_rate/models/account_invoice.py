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
        compute='_compute_rate',
        store=True,
    )

    @api.multi
    @api.depends('currency_id', 'date_invoice')
    def _compute_rate(self):
        currency_obj = self.env['res.currency']
        for inv in self:
            currency_id = inv.currency_id.id
            currency = currency_obj.browse(currency_id)
            rate = currency.with_context(
                date=inv.date_invoice)._get_current_rate(
                inv.date_invoice, None)
            inv.rate = rate[currency_id]
