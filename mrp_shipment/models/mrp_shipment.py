# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.addons import decimal_precision as dp


class MrpShipment(models.Model):
    _name = 'mrp.shipment'
    _description = 'Shipment'
    _rec_name = 'reference'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('cancel', 'Cancelled'),
         ('confirm', 'In Progress'),
         ('done', 'Validated'),
         ('finished', 'Finished')],
        string=_(u'Status'),
        readonly=True,
        select=True,
        default='draft',
        copy=False
    )
    folio = fields.Char(
        string='Folio',
        required=True,
        readonly=True,
        copy=False,
        default='new',
    )
    reference = fields.Text(
        string=_(u'Reference'),
        required=True,
    )
    date = fields.Date(
        string=_(u'Date of shipment'),
        default=fields.Date.today
    )
    departure_date = fields.Date(
        string=_(u'Departure date'),
        default=fields.Date.today
    )
    meters = fields.Float(
        string=_(u'Meters'),
        compute='_compute_meters'
    )
    freight = fields.Float(
        string=_(u'Freight'),
        compute='_compute_meters',
        digits_compute=dp.get_precision('Account'),
    )
    amount = fields.Float(
        string=_(u'Amount'),
        compute='_compute_meters',
        digits_compute=dp.get_precision('Account'),
    )
    line_ids = fields.One2many(
        'mrp.shipment.line',
        'shipment_id',
        string=_(u'Shipment Products'),
        readonly=False,
        states={'done': [('readonly', True)]},
        help="Shipment Lines.",
        copy=True
    )
    sale_ids = fields.One2many(
        'mrp.shipment.sale',
        'shipment_id',
        string=_(u'Shipment Order'),
        readonly=False,
        states={'done': [('readonly', True)]},
        copy=True
    )

    @api.depends('line_ids', 'line_ids.quantity_shipped')
    def _compute_meters(self):
        for shipment in self:
            meters = 0
            freight = 0
            amount = 0
            for line in shipment.line_ids:
                meters += (line.product_id.volume * line.quantity_shipped)
                freight += (line.order_line_id.freight_amount /
                            line.order_line_id.product_uom_qty) * \
                    line.quantity_shipped
                amount += (line.order_line_id.net_sale /
                           line.order_line_id.product_uom_qty) * \
                    line.quantity_shipped
            shipment.meters = meters
            shipment.freight = freight
            shipment.amount = amount

    @api.model
    def create(self, vals):
        if vals.get('folio', 'new') == 'new':
            vals['folio'] = self.env['ir.sequence'].next_by_code(
                'mrp.shipment') or '/'
        return super(MrpShipment, self).create(vals)

    @api.multi
    def unlink(self):
        for shipment in self:
            if shipment.state != 'cancel':
                raise ValidationError(_("You can only delete canceled \
                    shipments"))
        return super(MrpShipment, self).unlink()

    @api.multi
    def prepare_shipment(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def done(self):
        ship_line_obj = self.env['mrp.shipment.line']
        ship_sale_obj = self.env['mrp.shipment.sale']
        for ship in self:
            for line in ship.line_ids:
                sale_order_id = line.sale_order_id
                if line.quantity_shipped == 0:
                    line.unlink()
                    ship_line = ship_line_obj.search([
                        ('sale_order_id', '=', sale_order_id.id),
                        ('shipment_id', '=', ship.id)])
                    if not ship_line:
                        ship_sale = ship_sale_obj.search([
                            ('sale_id', '=', sale_order_id.id),
                            ('shipment_id', '=', ship.id)])
                        if ship_sale:
                            ship_sale.unlink()
            ship.state = 'done'
        return True

    @api.multi
    def cancel(self):
        for ship in self:
            for line in ship.line_ids:
                line.quantity_shipped = 0
            ship.state = 'cancel'
        return True

    @api.multi
    def finished(self):
        shipment_line_obj = self.env['mrp.shipment.line']
        for ship in self:
            for line in ship.line_ids:
                sale_line = line.order_line_id
                shipment_line = shipment_line_obj.search(
                    [('order_line_id', '=', sale_line.id),
                     ('id', '!=', line.id)])
                qty_shipment = 0
                for ship_line in shipment_line:
                    qty_shipment += ship_line.quantity_shipped
                qty_invoiced = sale_line.qty_invoiced - qty_shipment
                if line.quantity_shipped > qty_invoiced:
                    line.quantity_shipped = qty_invoiced
            ship.state = 'finished'
        return True

    @api.multi
    def add(self):
        return {
            'name': 'Add Sale Order',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.shipment.sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
        }


class MrpShipmentSale(models.Model):
    _name = 'mrp.shipment.sale'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
    )
    shipment_id = fields.Many2one(
        'mrp.shipment',
        string=_(u'Shipment'),
        ondelete='cascade',
        select=True)
    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
        related='sale_id.partner_id'
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
        related='sale_id.partner_shipping_id'
    )
    country_id = fields.Many2one(
        'res.country',
        string=_(u'Country'),
        related='partner_shipping_id.country_id',
        store=True,
    )
    state_id = fields.Many2one(
        'res.country.state',
        string=_(u'State'),
        related='partner_shipping_id.state_id',
        store=True,
    )
    city = fields.Char(
        string=_(u'City'),
        related='partner_shipping_id.city',
        store=True,
    )
    line_ids = fields.One2many(
        'mrp.shipment.line',
        'shipment_sale_id',
        string=_(u'Shipment Line'),
        readonly=False,
        copy=True
    )

    @api.multi
    def unlink(self):
        for sale in self:
            for line in sale.line_ids:
                if line.quantity_shipped != 0:
                    raise ValidationError(_("The quantity shipped in a \
                        line is different from 0"))
        return super(MrpShipmentSale, self).unlink()


class MrpShipmentLine(models.Model):
    _name = 'mrp.shipment.line'
    _description = 'Shipment line'

    shipment_id = fields.Many2one(
        'mrp.shipment',
        string=_(u'Shipment'),
        ondelete='cascade',
        select=True
    )
    shipment_sale_id = fields.Many2one(
        'mrp.shipment.sale',
        string=_(u'Shipment Sale'),
        ondelete='cascade',
        select=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
        related='shipment_sale_id.partner_id',
        store=True,
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string=_(u'Customer'),
        related='shipment_sale_id.partner_shipping_id'
    )
    country_id = fields.Many2one(
        'res.country',
        string=_(u'Country'),
        related='partner_shipping_id.country_id',
        store=True,
    )
    state_id = fields.Many2one(
        'res.country.state',
        string=_(u'State'),
        related='partner_shipping_id.state_id',
        store=True,
    )
    city = fields.Char(
        string=_(u'City'),
        related='partner_shipping_id.city',
        store=True,
    )
    street = fields.Char(
        string=_(u'Street'),
        related='partner_shipping_id.street',
        store=True,
    )
    street2 = fields.Char(
        string=_(u'Street2'),
        related='partner_shipping_id.street2',
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
        store=True
    )
    product_code = fields.Char(
        string=_(u'Code product'),
        related='product_id.default_code',
        store=True
    )
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

    @api.multi
    def unlink(self):
        for line in self:
            if line.quantity_shipped != 0:
                raise ValidationError(_("The quantity shipped in a \
                    line is different from 0"))
        return super(MrpShipmentLine, self).unlink()
