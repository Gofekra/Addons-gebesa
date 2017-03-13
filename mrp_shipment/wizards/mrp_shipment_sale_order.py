# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpShipmentSaleOrder(models.TransientModel):
    _name = 'mrp.shipment.sale.order'

    sale_ids = fields.Many2many(
        'sale.order',
        string=_('Sale Order'),
    )

    @api.multi
    def add_sale_order(self):
        shipment_obj = self.env['mrp.shipment']
        shipment_line_obj = self.env['mrp.shipment.line']
        ship_sale_obj = self.env['mrp.shipment.sale']
        active_ids = self._context.get('active_ids', []) or []
        shipment = shipment_obj.browse(active_ids)
        order_line_id = []
        sale_id = []
        for sale in shipment.sale_ids:
            sale_id.append(sale.sale_id.id)
        for lines in shipment.line_ids:
            order_line_id.append(lines.order_line_id.id)
        for shipment_sale in self:
            for sale in shipment_sale.sale_ids:
                if sale.state == "done":
                    for line in sale.order_line:
                        if line.id not in order_line_id:
                            if line.missing_quantity > 0:
                                if sale.id not in sale_id:
                                    ship_sale = ship_sale_obj.create({
                                        'sale_id': sale.id,
                                        'shipment_id': shipment.id
                                    })
                                    sale_id.append(sale.id)
                                else:
                                    ship_sale = ship_sale_obj.search([
                                        ('sale_id', '=', sale.id),
                                        ('shipment_id', '=', shipment.id)
                                    ])
                                shipment_line_obj.create({
                                    'shipment_id': shipment.id,
                                    'shipment_sale_id': ship_sale.id,
                                    'partner_id': line.order_partner_id.id,
                                    'sale_order_id': sale.id,
                                    'order_line_id': line.id,
                                    'product_id': line.product_id.id,
                                    'quantity': line.missing_quantity,
                                    'quantity_shipped': line.missing_quantity,
                                })
