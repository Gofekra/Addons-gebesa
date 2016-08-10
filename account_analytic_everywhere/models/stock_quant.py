# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u'Analytic Account'),
    )

    # def _prepare_account_move_line(self, cr, uid, move, qty, cost,
    #                                credit_account_id, debit_account_id,
    #                                context=None):
    #     """
    #     Generate the account.move.line values to post to
    #     track the stock valuation difference due to the
    #     processing of the given quant.
    #     """
    #     if context is None:
    #         context = {}

    #     move_lines = super(
    #         StockQuant, self)._prepare_account_move_line(
    #             cr, uid, move, qty, cost,
    #             credit_account_id, debit_account_id, context)

    #     analytic_id = move.warehouse_id.account_analytic_id.id or False

    #     move_lines2 = []
    #     for line in move_lines:
    #         values = line[2]
    #         values.update({'analytic_account_id': analytic_id})
    #         move_lines2.append((0, 0, values))

    #     return move_lines2
