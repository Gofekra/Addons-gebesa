# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    quantity_shipped = fields.Float(
        string=_(u'Quantity shipped'),
        compute='_quantity_shipped',
        store=True,
    )

    missing_quantity = fields.Float(
        string=_(u'missing quantity'),
        compute='_missing_quantity',
        store=True,
    )

    shipment_line_ids = fields.One2many(
        'mrp.shipment.line',
        'order_line_id',
        string=_('Shipment'),
    )

    @api.depends('shipment_line_ids.quantity_shipped')
    def _quantity_shipped(self):
        for line in self:
            domain = [('order_line_id', '=', line.id)]

            shipment_line = self.env['mrp.shipment.line'].search(domain)
            quantity_shipped = 0

            for shipment in shipment_line:
                quantity_shipped += shipment.quantity_shipped

            line.quantity_shipped = quantity_shipped

    @api.depends('quantity_shipped')
    def _missing_quantity(self):
        for line in self:
            line.missing_quantity = line.product_uom_qty - \
                line.quantity_shipped
