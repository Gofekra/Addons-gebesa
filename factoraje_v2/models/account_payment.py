# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    prepayment_type = fields.Selection(
        selection_add=[('factoraje', _('Factoraje'))],
        default='normal',
    )

    def _create_move_line_factoraje(self, move, account, debit, credit,
                                    invoice, currency_id, amount_currency):
        move_line_dict = {
            'account_id': account,
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'currency_id': currency_id,
            'amount_currency': amount_currency,
            'debit': debit,
            'credit': credit,
            'name': 'Factoraje: ' + invoice,
            'date': self.payment_date,
            'move_id': move,
            'payment_id': self.id,
        }

        return move_line_dict

    def _create_payment_entry(self, amount):
        aml_obj = self.env['account.move.line'].with_context(
            check_move_validity=False)
        aag_obj = self.env['account.account.global']
        move = super(AccountPayment, self)._create_payment_entry(amount)

        if self.prepayment_type == 'factoraje':
            move.button_cancel()

            if self.invoice_ids and all(
                    [x.currency_id == self.invoice_ids[0].currency_id
                     for x in self.invoice_ids]):
                invoice_currency = self.invoice_ids[0].currency_id
                invoice = self.invoice_ids[0].number

            debit, credit, amount_currency, currency_id = aml_obj.with_context(
                date=self.payment_date).compute_amount_fields(
                amount, self.currency_id, self.company_id.currency_id,
                invoice_currency)

            account = aag_obj.search(
                [('name', '=', 'fac'),
                 ('code', '=', 2)], limit=1).account_id.id
            res = self._create_move_line_factoraje(move.id, account, credit,
                                                   debit, invoice,
                                                   currency_id,
                                                   amount_currency)
            aml_obj.create(res)

            account = aag_obj.search(
                [('name', '=', 'fac_ban'),
                 ('code', '=', 1)], limit=1).account_id.id
            res = self._create_move_line_factoraje(move.id, account, debit,
                                                   credit * .8, invoice,
                                                   currency_id,
                                                   amount_currency)
            aml_obj.create(res)

            account = self.journal_id.default_credit_account_id.id
            res = self._create_move_line_factoraje(move.id, account, debit,
                                                   credit * .2, invoice,
                                                   currency_id,
                                                   amount_currency)
            aml_obj.create(res)

            move.post()

        return move
