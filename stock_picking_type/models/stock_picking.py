# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_move_type_id = fields.Many2one(
        'stock.move.type',
        string=_(u'Type of move'),
    )

    @api.onchange('stock_move_type_id',)
    def _onchange_stock_move_type_id(self):
        if self.stock_move_type_id.code in ('E4', 'S4'):
            if self.stock_move_type_id.code == 'E4':
                self.picking_type_id = self.env.user.employee_ids.\
                    default_warehouse_id.in_type_id.id
            else:
                self.picking_type_id = self.env.user.employee_ids.\
                    default_warehouse_id.out_type_id.id
