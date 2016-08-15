# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    stock_move_type_id = fields.Many2one(
        'stock.move.type',
        compute='_get_move_type',
        store=True,
        string=_(u'Type of move'),
    )

    @api.multi
    @api.depends('procurement_id', 'move_dest_id', 'production_id', 'purchase_line_id', 'raw_material_production_id')
    def _get_move_type(self):
        mpf_type = False
        for move in self:
            if move.procurement_id and move.procurement_id.id:
                if move.procurement_id.sale_line_id:
                    mpf_type = move.env.ref(
                        'stock_picking_type.mpf_tipomov_S1', False)
            if move.move_dest_id:
                mpf_type = move.env.ref(
                    'stock_picking_type.mpf_tipomov_T1', False)
            if move.purchase_line_id:
                mpf_type = move.env.ref(
                    'stock_picking_type.mpf_tipomov_E2', False)
            if move.raw_material_production_id:
                mpf_type = move.env.ref(
                    'stock_picking_type.mpf_tipomov_S5', False)
            if move.production_id:
                mpf_type = move.env.ref(
                    'stock_picking_type.mpf_tipomov_E5', False)
            move.stock_move_type_id = mpf_type

    # @api.model
    # def _prepare_procurement_from_move(self, move):
    #     res = super(StockMove, self)._prepare_procurement_from_move(move)
    #     return res
