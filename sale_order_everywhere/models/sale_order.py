# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        group_obj = self.env['procurement.group']
        move_obj = self.env['stock.move']
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            group = group_obj.search([('sale_id', '=', order.id)])
            for procurement in group.procurement_ids:
                procurement.sale_id = group.sale_id
                if procurement.production_id:
                    procurement.production_id.sale_id = group.sale_id
            moves = move_obj.search([('group_id', '=', group.id)])
            for move in moves:
                move.sale_id = group.sale_id
        return res
