# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    segment_status = fields.Selection(
        [('no_segment', _('No Segment')),
         ('partial_segment', _('Partial Segment')),
         ('total_segment', _('Total Segment'))],
        string=_("Segment Status"),
        default='no_segment',
        compute='_compuete_segment_status'
    )

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )

    production_status = fields.Selection(
        compute='_compuete_production_status',
    )

    @api.model
    def _prepare_procurement_group(self):
        res = super(SaleOrder, self)._prepare_procurement_group()
        res['sale_id'] = self.id
        return res

    @api.depends('related_segment')
    def _compuete_segment_status(self):
        production_obj = self.env['mrp.production']
        prod = production_obj.search([('sale_id', '=', self.id)])
        prod_seg = production_obj.search([('sale_id', '=', self.id),
                                          ('segment_line_ids', '!=', False)])
        ## ---> Set BreakPoint
        import pdb;
        pdb.set_trace()
        if not prod_seg:
            self.segment_status = 'no_segment'
        elif len(prod) == len(prod_seg):
            self.segment_status = 'total_segment'
        else:
            self.segment_status = 'partial_segment'

    @api.depends('order_line.segment_qty')
    def _compuete_production_status(self):
        for sale in self:
            seg_qty = 0
            pro_qty = 0
            for line in sale.order_line:
                seg_qty += line.segment_qty
                pro_qty += line.product_uom_qty
            if seg_qty == pro_qty:
                sale.production_status = 'total_production'
            elif seg_qty == 0:
                sale.production_status = 'no_production'
            else:
                sale.production_status = 'partial_production'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    segment_qty = fields.Float(
        string='Segmented quantity',
    )
