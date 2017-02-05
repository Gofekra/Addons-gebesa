# -*- coding: utf-8 -*-
# © <2016> <Cesar Barron>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError


class MrpSegment(models.Model):
    _name = "mrp.segment"
    _description = "MRP Segment"
    _rec_name = 'folio'

    def _default_stock_location(self):
        try:
            warehouse = self.env['ir.model.data'].get_object(
                'stock', 'warehouse0')
            return warehouse.lot_stock_id.id
        except:
            return False

    name = fields.Char(
        string=_('Segment Reference'),
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help=_('Segment Name.'))

    folio = fields.Char(
        string='Folio',
        required=True,
        readonly=True,
        copy=False,
        default='new',
    )

    date = fields.Datetime(
        string=_('Segment Date'),
        required=True,
        readonly=True,
        default=fields.Datetime.now,
        help=_('The date that will be used for the segment.'))

    state = fields.Selection(
        [('draft', 'Draft'),
         ('cancel', 'Cancelled'),
         ('confirm', 'In Progress'),
         ('done', 'Validated')],
        string=_('Status'),
        readonly=True,
        select=True,
        default='draft',
        copy=False)

    location_id = fields.Many2one(
        'stock.location',
        string=_('Segment Location'),
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=_default_stock_location)

    company_id = fields.Many2one(
        'res.company',
        string=_('Company'),
        required=True,
        select=True,
        readonly=True,
        default=lambda self: self.env.user.company_id,
        states={'draft': [('readonly', False)]})

    line_ids = fields.One2many(
        'mrp.segment.line',
        'segment_id',
        string=_('Manufacturing Order Line'),
        readonly=False,
        states={'done': [('readonly', True)]},
        help=_("Segment Lines."),
        copy=True,
        ondelete='cascade')

    product_lines_ids = fields.One2many(
        'mrp.production.product.line',
        'production_id',
        compute='_compute_product_lines_ids',
        string='Scheduled goods',
    )

    @api.depends('line_ids.mrp_production_id')
    def _compute_product_lines_ids(self):
        product_lines = []
        for line in self.line_ids:
            for pro_lin in line.mrp_production_id.product_lines:
                product_lines.append(pro_lin.id)
        self.product_lines_ids = product_lines

    _sql_constraints = [
        ('folio_uniq', 'unique (folio)',
         'This field must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('folio', 'New') == 'New':
            vals['folio'] = self.env['ir.sequence'].next_by_code(
                'mrp.segment') or '/'
        return super(MrpSegment, self).create(vals)

    @api.multi
    def prepare_segment(self):
        for segment in self:
            line_ids = [line.id for line in segment.line_ids]
            if not line_ids:
                vals = self._get_segment_lines()

                for production_line in vals:
                    self.env['mrp.segment.line'].create(production_line)

        return self.write({'state': 'confirm'})

    def _get_segment_lines(self):
        domain = [('segment_line_ids', '=', False),
                  ('location_dest_id', '=', self.location_id.id),
                  ('state', 'in', ["confirmed", "ready"])]

        segment_lines = self.env['mrp.production'].search(domain)

        vals = []
        for produ in segment_lines:
            product_line = dict(
                (fn, 0.0) for fn in [
                    'segment_id', 'mrp_production_id',
                    'product_id', 'sale_name', 'product_qty',
                    'quantity'])

            product_line['segment_id'] = self.id
            product_line['mrp_production_id'] = produ.id
            product_line['product_id'] = produ.product_id.id
            product_line['sale_name'] = produ.origin
            product_line['product_qty'] = produ.product_qty
            product_line['quantity'] = 0
            vals.append(product_line)
        return vals

    @api.multi
    def process_segment(self):
        produce_obj = self.env['mrp.production']
        for produ in self.line_ids:
            if produ.quantity > 0:
                produce_obj.action_produce(produ.mrp_production_id.id,
                                           produ.quantity,
                                           'consume_produce',
                                           )
        done = True
        for produ in self.line_ids:
            if produ.manufacture_qty > 0:
                done = False
            produ.quantity = 0
        if done:
            self.state = 'done'
        return True


class MrpSegmentLine(models.Model):
    _name = "mrp.segment.line"
    _description = "Segmentation Line"
    _order = 'segment_id'

    segment_id = fields.Many2one(
        'mrp.segment',
        string=_('Segmentation'),
        ondelete='cascade',
        select=True,
        readonly=True,)

    mrp_production_id = fields.Many2one(
        'mrp.production',
        required=True,
        string=_('Manufacturing Order'),
        readonly=True,
    )

    state = fields.Selection(
        [('draft', _('New')),
         ('cancel', _('Cancelled')),
         ('confirmed', _('Awaiting Raw Materials')),
         ('ready', _('Ready to Produce')),
         ('in_production', _('Production Started')),
         ('done', _('Done'))],
        string=_("Status"),
        readonly=True,
        related='mrp_production_id.state',
    )

    product_id = fields.Many2one(
        'product.product',
        string=_('Product'),
        readonly=True,
    )

    product_code = fields.Char(
        string=_('Code Product'),
        related='product_id.default_code',
        store=True,
        readonly=True,)

    product_name = fields.Char(
        string=_('Name Product'),
        related='product_id.name',
        store=True,
        readonly=True,)

    product_weight = fields.Float(
        string=_('Weight Product'),
        related='product_id.weight',
        store=True,
        readonly=True,)

    product_volume = fields.Float(
        string=_('Volume Product'),
        related='product_id.volume',
        store=True,
        readonly=True,)

    standard_cost = fields.Float(
        string=_('Standard Cost'),
        compute='_compute_standard_price',
        store=True,
        readonly=True,
    )

    product_uom = fields.Many2one(
        'product.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        readonly=True,
    )

    sale_name = fields.Char(
        string=_('Sale Order'),
        readonly=True,
    )

    product_qty = fields.Float(
        string=_('Product quantity'),
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True,
    )

    manufacture_qty = fields.Float(
        string=_('Quantity to manufacture'),
        compute='_compute_manufacture_qty',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True,
    )

    quantity = fields.Float(
        string=_('Done'),
        digits=dp.get_precision('Product Unit of Measure')
    )

    @api.constrains('quantity')
    def _check_qty_segmented(self):
        for line in self:
            if line.quantity > line.manufacture_qty:
                raise UserError(_("The quantity available is less than \n"
                                  "the quantity segmented"))

    @api.depends('product_id')
    def _compute_standard_price(self):
        for line in self:
            line.standard_cost = line.product_id.standard_price

    @api.depends('mrp_production_id.move_created_ids.product_uom_qty')
    def _compute_manufacture_qty(self):
        for line in self:
            line.manufacture_qty = line.mrp_production_id.move_created_ids.\
                product_uom_qty

    @api.model
    def create(self, vals):
        production_obj = self.env['mrp.production']
        segment_obj = self.env['mrp.segment']
        procurement_obj = self.env['procurement.order']
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        purchase_obj = self.env['purchase.order']
        production = production_obj.browse(vals['mrp_production_id'])
        segment = segment_obj.browse(vals['segment_id'])
        procurement = procurement_obj.search([
            ('origin', 'like', production.name)])
        for proc in procurement:
            proc.related_segment += segment.folio + ', '
        picking = picking_obj.search([
            ('origin', 'like', production.name)])
        for pick in picking:
            pick.related_segment += segment.folio + ', '
        move = move_obj.search([
            ('origin', 'like', production.name)])
        for mov in move:
            mov.related_segment += segment.folio + ', '
        purchase = purchase_obj.search([
            ('origin', 'like', production.name)])
        for pur in purchase:
            pur.related_segment += segment.folio + ', '
        return super(MrpSegmentLine, self).create(vals)
