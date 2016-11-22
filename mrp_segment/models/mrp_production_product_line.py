# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

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

    segment_line_ids = fields.One2many(
        'mrp.segment.line',
        'mrp_production_line_id',
        string=_('Segment'),
    )

    @api.depends('segment_line_ids.qty_segmented')
    def _qty_segmented(self):
        for line in self:
            domain = [('mrp_production_line_id', '=', line.id)]

            segment_line = self.env['mrp.segment.line'].search(domain)
            qty_segmented = 0

            for segment in segment_line:
                qty_segmented += segment.qty_segmented

            line.qty_segmented = qty_segmented

    @api.depends('qty_segmented')
    def _missing_qty(self):
        for line in self:
            line.missing_qty = line.product_qty - \
                line.qty_segmented
