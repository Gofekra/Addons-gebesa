# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    status_review = fields.Selection([
        ('no_review', _('No Review')),
        ('review', _('Review'))],
        string=_('Warehouse Review'),
        default='no_review',
        store=True)

    @api.multi
    def status_review(self):
        for order in self:
            if order.status_review == 'review':
                raise UserError(_("This purchase order has already"
                                  "been reviewed"))
            else:
                self.write({'status_review': 'review'})
        return True
