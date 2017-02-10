# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    type_adjustment_id = fields.Many2one('type.adjustment',
                                         string=_('Type Adjustment'),
                                         store=True,)

    @api.model
    def create(self, vals):
        ctx = self.env.context.copy()
        if 'default_stock_move_type_id' in ctx.keys():
            move_type = self.env['stock.move.type'].browse(
                [ctx['default_stock_move_type_id']])
            if move_type:
                if move_type.code in ('E4', 'S4'):
                    warehouse = self.env.user.employee_ids.default_warehouse_id
                    if move_type.code == 'E4':
                        default = warehouse.in_type_id.id
                    else:
                        default = warehouse.out_type_id.id
                    ctx.update({'default_picking_type_id': default})
        res = super(StockPicking, self.with_context(ctx)).create(vals)
        return res
