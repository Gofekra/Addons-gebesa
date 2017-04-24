# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pending_qty = fields.Float(
        'Pending',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_pending_qty',
        store=True,
    )

    @api.model
    @api.depends('product_uom_qty', 'qty_delivered')
    def _compute_pending_qty(self):
        for line in self:
            pending_qty = line.product_uom_qty - line.qty_delivered
            line.pending_qty = pending_qty
