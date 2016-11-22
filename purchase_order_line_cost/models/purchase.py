# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def _onchange_order_line(self):
        for purchase in self:
            domain = []
            for line in purchase.order_line:
                partner = []
                seller_ids = line.product_id.seller_ids
                if not seller_ids:
                    return {'domain': {'partner_id': [('id', 'in', '[]')]}}
                if not domain:
                    for seller in seller_ids:
                        domain.append(seller.name.id)
                else:
                    for seller in seller_ids:
                        if seller.name.id in domain:
                            partner.append(seller.name.id)
                    domain = partner
            if purchase.partner_id.id not in domain:
                purchase.partner_id = None
        return {'domain': {'partner_id': [('id', 'in', domain)]}}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    standard_price = fields.Float(
        string=_('Standard price'),
        related='product_id.standard_price'
    )
