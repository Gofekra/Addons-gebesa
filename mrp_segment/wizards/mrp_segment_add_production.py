# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpSegmentAddProduction(models.TransientModel):
    _name = 'mrp.segment.add.production'

    location_id = fields.Many2one(
        'stock.location',
        string=_('Segment location'),
    )
    production_ids = fields.Many2many(
        'mrp.production',
        string=('Production'),
    )

    @api.multi
    def add_production(self):
        segment_obj = self.env['mrp.segment']
        segment_line_obj = self.env['mrp.segment.line']
        active_ids = self._context.get('active_ids', []) or []
        segment = segment_obj.browse(active_ids)
        for produ in self.production_ids:
            segment_line_obj.create({
                'segment_id': segment.id,
                'mrp_production_id': produ.id,
                'product_id': produ.product_id.id,
                'sale_name': produ.origin,
                'product_qty': produ.product_qty,
                'manufacture_qty': produ.product_qty,
                'quantity': 0,
                'standard_cost': produ.product_id.standard_price,
            })
