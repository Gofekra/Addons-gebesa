# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()

        move_obj = self.pool.get('account.move')
        picking_obj = self.pool.get('stock.picking')

        res = super(StockMove, self).action_done(cr, uid, ids, context=ctx)

        move_ids = []
        for move in self.browse(cr, uid, ids, context=context):
            picking_id = move.picking_id
        move_ids = move_obj.search(
            cr, uid, [('ref', '=', picking_id.name)])
        data = picking_obj.browse(cr, uid, picking_id.id, context=ctx)
        data.am_ids = False
        data.am_ids = move_ids

        return res
