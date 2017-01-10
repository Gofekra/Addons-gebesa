# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    segment_line_ids = fields.One2many(
        'mrp.segment.line',
        'mrp_production_id',
        string=_('Segment'),
    )

    qty_segmented = fields.Float(
        string=_('Quantity Segmented'),
        compute='_qty_segmented',
        store=True,
    )

    missing_qty = fields.Float(
        string=_('Missing Quantity'),
        compute='_missing_qty',
        store=True,
    )

    @api.depends('segment_line_ids.qty_segmented')
    def _qty_segmented(self):
        for production in self:
            domain = [('mrp_production_id', '=', production.id)]

            segment_line = self.env['mrp.segment.line'].search(domain)
            qty_segmented = 0

            for segment in segment_line:
                qty_segmented += segment.qty_segmented

            production.qty_segmented = qty_segmented

    @api.depends('qty_segmented', 'product_qty')
    def _missing_qty(self):
        for production in self:
            production.missing_qty = production.product_qty - \
                production.qty_segmented
