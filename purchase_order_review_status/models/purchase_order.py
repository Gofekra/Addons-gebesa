# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    review = fields.Selection([
        ('no_review', _('No Review')),
        ('yes_review', _('Review'))],
        string=_('Warehouse Review'),
        track_visibility='onchange',
        default='no_review')

    @api.multi
    def action_review(self):
        for order in self:
            if order.review == 'no_review':
                self.write({'review': 'yes_review'})
                for line in order.order_line:
                    reviewed = True
                    line.reviewed = reviewed
            else:
                raise UserError(_("This purchase order has already "
                                  "been reviewed by the Warehouse Manager"))
        return True

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.review == 'no_review':
                raise UserError(_("Can not confirm the order until it \
                    is reviewed"))
        return super(PurchaseOrder, self).button_confirm()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    reviewed = fields.Boolean(
        string=_('Valid'),
        track_visibility='onchange')

    origin = fields.Char(
        related='order_id.origin',
        readonly=True,
        stored=True)

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        related='order_id.warehouse_id',
        string='Warehouse',
        store=True,
        readonly=True)

    @api.multi
    @api.constrains('reviewed')
    def _update_valid_po(self):
        for line in self:
            lines = len(line.order_id.order_line)
            valid_lines = len(
                self.env['purchase.order.line'].search(
                    [('order_id', '=', line.order_id.id),
                     ('reviewed', '=', True)]))
            if valid_lines == lines:
                line.order_id.review = 'yes_review'
            else:
                line.order_id.review = 'no_review'
