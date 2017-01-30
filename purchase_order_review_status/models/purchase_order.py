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
            else:
                raise UserError(_("This purchase order has already "
                                  "been reviewed by the Warehouse Manager"))
        return True


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

    @api.onchange('reviewed')
    def _update_valid_po(self):
        lines = len(self.order_id.order_line)
        valid_lines = len(
            self.env['purchase.order.line'].search(
                [('id', '=', self.order_id.id),
                 ('reviewed', '=', True)]))
        if valid_lines == lines:
            self.order_id.review = 'yes_review'
        else:
            self.order_id.review = 'no_review'
