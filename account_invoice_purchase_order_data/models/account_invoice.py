# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    purchase_ids = fields.Many2many(
        'purchase.order',
        string=_(u'Purchase Order'),
    )

    @api.onchange('purchase_id')
    def _onchange_purchase_order(self):
        if not self.purchase_id:
            return {}
        self.purchase_ids = [self.purchase_id.id]
