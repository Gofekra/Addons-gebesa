# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def picking_account_move_generate(self):
        for pick in self:
            for move in pick.move_lines:
                import pdb; pdb.set_trace()
                    
