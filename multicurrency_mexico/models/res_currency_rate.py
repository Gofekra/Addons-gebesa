# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    rate_mex = fields.Float(
        string=_('Rate mexico'),
        digits=(12, 6),
    )

    @api.onchange('rate_mex')
    def _onchange_rate_mex(self):
        if self.rate_mex != 0.00:
            self.rate = 1 / self.rate_mex
        else:
            self.rate = 0.00
