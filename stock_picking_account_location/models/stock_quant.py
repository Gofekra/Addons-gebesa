# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _get_accounting_data_for_valuation(self, move):
        journal_id, acc_src, acc_dest, acc_valuation = super(
            StockQuant, self)._get_accounting_data_for_valuation(move)

        acc_valuation = move.location_id.account_id.id
        if not acc_valuation:
            raise ValidationError(
                _(u"It has not defined the inventory \
                  account in location %s.") %
                (move.location_id.name))

        return journal_id, acc_src, acc_dest, acc_valuation
