# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp import SUPERUSER_ID


class PurchaseConfiguration(models.TransientModel):
    _inherit = 'purchase.config.settings'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id
    )
    has_default_company = fields.Boolean(
        readonly=True,
        default=lambda self: self._default_has_default_company()
    )
    purchase_price_account_id = fields.Many2one(
        'account.account',
        string=_('Default Account Purchase Price Difference'),
    )

    @api.model
    def _default_has_default_company(self):
        count = self.env['res.company'].search_count([])
        return bool(count == 1)

    @api.v7
    def set_default_account_product_price(self, cr, uid, ids, context=None):
        purchase_price_account_id = self.browse(
            cr, uid, ids, context=context).purchase_price_account_id
        res = self.pool.get('ir.values').set_default(
            cr, SUPERUSER_ID, 'purchase.config.settings',
            'purchase_price_account_id', purchase_price_account_id.id)
        return res
