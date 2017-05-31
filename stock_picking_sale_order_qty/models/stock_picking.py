# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):
        bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        for pick in self:
            if pick.location_dest_id.usage != 'customer':
                continue
            if not pick.sale_id:
                continue
            products = {}
            for line in pick.sale_id.order_line:
                product = line.product_id
                bom = bom_obj.search([
                    ('product_id', '=', product.id),
                    ('active', '=', True)
                ])
                if bom.type == 'phantom':
                    for bom_l in bom.bom_line_ids:
                        qty = line.product_uom_qty * bom.product_qty * bom_l.product_qty
                        if bom_l.product_id.id in products.keys():
                            products[bom_l.product_id.id] += qty
                        else:
                            products[bom_l.product_id.id] = qty
                else:
                    qty = line.product_uom_qty
                    if line.product_id.id in products.keys():
                        products[line.product_id.id] += qty
                    else:
                        products[line.product_id.id] = qty
            for move in pick.move_lines_related:
                products[move.product_id.id] -= move.product_uom_qty
            if pick.related_segment:
                for move in pick.related_segment.move_lines_related:
                    products[move.product_id.id] -= move.product_uom_qty
            for prod in products:
                if products[prod] > 0:
                    product = product_obj.browse([prod])
                    raise UserError(_('Missing %s %s') % (
                        products[prod], product.name))
        return super(StockPicking, self).do_new_transfer()
