# -*- coding: utf-8 -*-
# © <2016> <Cesar Barron>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp.exceptions import UserError


class MrpSegment(models.Model):
    _name = "mrp.segment"
    _description = "MRP Segment"
    _rec_name = 'name'

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
        copy=True)

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
        domain = [('missing_quantity', '>', 0),
                  ('production_id.location_dest_id', '=', self.location_id.id),
                  ('production_id.state', 'in', ["confirmed", "ready"])]

        segment_lines = self.env['mrp.production.product.line'].search(domain)

        vals = []
        for line in segment_lines:
            product_line = dict(
                (fn, 0.0) for fn in [
                    'segment_id', 'mrp_production_id',
                    'product_id', 'quantity', 'sale_name',
                    'mrp_production_line_id'])

            product_line['segment_id'] = self.id
            product_line['mrp_production_id'] = line.production_id.id
            product_line['product_id'] = line.product_id.id
            product_line['quantity'] = line.missing_qty
            product_line['sale_name'] = line.production_id.sale_name
            product_line['mrp_production_line_id'] = line.id
            vals.append(product_line)
        return vals


class MrpSegmentLine(models.Model):
    _name = "mrp.segment.line"
    _description = "Segmentation Line"
    _order = 'segment_id'

    segment_id = fields.Many2one(
        'mrp.segment',
        string=_('Segmentation'),
        ondelete='cascade',
        select=True)

    mrp_production_id = fields.Many2one(
        'mrp.production',
        string=_('Manufacturing Order'),
    )

    mrp_production_line_id = fields.Many2one(
        'mrp.production.product.line',
        string=_('Manufacturing Order Line'),
    )

    product_id = fields.Many2one(
        'product.product',
        string=_('Product'),
    )

    product_code = fields.Char(
        string=_('Code Product'),
        related='product_id.default_code',
        store=True)

    product_name = fields.Char(
        string=_('Name Product'),
        related='product_id.name',
        store=True)

    product_weight = fields.Float(
        string=_('Weight Product'),
        related='product_id.weight',
        store=True)

    product_volume = fields.Float(
        string=_('Name Product'),
        related='product_id.volume',
        store=True)

    standard_cost = fields.Float(
        string=_('Standard Cost'),
        related='product_id.standard_price',
    )

    quantity = fields.Float(
        string=_('Quantity'),
    )

    sale_name = fields.Char(
        string=_('Sale Order'))

    qty_segmented = fields.Float(
        string=_('Quantity Segmented'))

    @api.constrains('qty_segmented')
    def _check_qty_segmented(self):
        for line in self:
            if line.qty_segmented > line.quantity:
                raise UserError(_("The quantity available is less than \n"
                                  "the quantity segmented"))
