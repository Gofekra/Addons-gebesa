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
