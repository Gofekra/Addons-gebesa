# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MrpShipment(models.Model):
    _name = 'mrp.shipment'
    _description = 'Shipment'
    _rec_name = 'reference'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('cancel', 'Cancelled'),
         ('confirm', 'In Progress'),
         ('done', 'Validated')],
        string=_(u'Status'),
        readonly=True,
        select=True,
        default='draft',
        copy=False)

    reference = fields.Text(
        string=_(u'Reference'),
        required=True,
    )

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_(u'Warehouse'),
        required=True,
    )

    date = fields.Date(
        string=_(u'Date'),
        default=fields.Date.today
    )

    line_ids = fields.One2many(
        'mrp.shipment.line',
        'shipment_id',
        string=_(u'Shipment Products'),
        readonly=False,
        states={'done': [('readonly', True)]},
        help="Shipment Lines.",
        copy=True)

    @api.multi
    def prepare_shipment(self):
        for ship in self:
            # If there are revaluation lines already (e.g. from import),
            # respect those and set their actual cost
            line_ids = [line.id for line in ship.line_ids]
            if not line_ids:
                # compute the revaluation lines and create them
                vals = self._get_shipment_lines()

                for order_line in vals:
                    self.env['mrp.shipment.line'].create(order_line)

        return self.write({'state': 'confirm'})

    def _get_shipment_lines(self):
        domain = [('missing_quantity', '>', 0),
                  ('order_id.warehouse_id', '=', self.warehouse_id.id)]
        order_lines = self.env['sale.order.line'].search(domain)

        vals = []
        for line in order_lines:
            product_line = dict(
                (fn, 0.0) for fn in [
                    'shipment_id', 'partner_id',
                    'sale_order_id', 'product_id',
                    'quantity', 'order_line_id'])
            # replace the None the dictionary by False, because falsy
            # values are tested later on
            product_line['shipment_id'] = self.id
            product_line['partner_id'] = line.order_partner_id.id
            product_line['sale_order_id'] = line.order_id.id
            product_line['product_id'] = line.product_id.id
            product_line['order_line_id'] = line.id
            product_line['quantity'] = line.missing_quantity
            vals.append(product_line)
        return vals


class MrpShipmentLine(models.Model):
    _name = 'mrp.shipment.line'
    _description = 'Shipment line'

    shipment_id = fields.Many2one(
        'mrp.shipment',
        string=_(u'Shipment'),
        ondelete='cascade',
        select=True)

    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
    )

    country_id = fields.Many2one(
        'res.country',
        string=_(u'Country'),
        related='partner_id.country_id',
        store=True,
    )

    state_id = fields.Many2one(
        'res.country.state',
        string=_(u'State'),
        related='partner_id.state_id',
        store=True,
    )

    city = fields.Char(
        string=_(u'City'),
        related='partner_id.city',
        store=True,
    )

    street = fields.Char(
        string=_(u'Street'),
        related='partner_id.street',
        store=True,
    )

    street2 = fields.Char(
        string=_(u'Street2'),
        related='partner_id.street2',
        store=True,
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        string=_(u'Sale order'),
    )

    order_line_id = fields.Many2one(
        'sale.order.line',
        string=_(u'Sale order line '),
    )

    quantity = fields.Float(
        string=_(u'Quantity'),
    )

    quantity_shipped = fields.Float(
        string=_(u'Quantity shipped'),
    )

    product_id = fields.Many2one(
        'product.product',
        string=_(u'Product'),
    )

    product_name = fields.Char(
        string=_(u'Name product'),
        related='product_id.name',
        store=True)

    product_code = fields.Char(
        string=_(u'Code product'),
        related='product_id.default_code',
        store=True)

    standard_cost = fields.Float(
        string=_(u'Standard cost'),
        related='product_id.standard_price',
    )

    @api.constrains('quantity_shipped')
    def _check_quantity_shipped(self):
        for line in self:
            if line.quantity_shipped > line.quantity:
                raise ValidationError(_("The quantity available is less than \
                                      the quantity shipped"))
