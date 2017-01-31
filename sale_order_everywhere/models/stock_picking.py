# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('move_lines', 'move_lines.sale_id')
    def _compute_sale_id(self):
        for picking in self:
            sale_order = False
            for move in picking.move_lines:
                if move.sale_id:
                    sale_order = move.sale_id
                    break
            picking.sale_id = sale_order.id if sale_order else False
