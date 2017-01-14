# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u'Analytic Account'),
    )

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.type in ('in_invoice'):
                inv.asigna_analytic()
        return res

    def asigna_analytic(self):
        move = self.move_id

        for line in move.line_ids:
            if not line.analytic_account_id:
                line.analytic_account_id = self.account_analytic_id


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def _set_additional_fields(self, invoice):
        analytic = self.account_analytic_id
        super(AccountInvoiceLine, self)._set_additional_fields(invoice)
        self.account_analytic_id = analytic
