# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp import _, fields, models


class PurchaseConfiguration(models.TransientModel):
    _name = 'purchase.config.settings'
    _inherit = 'purchase.config.settings'

    purchase_price_account_id = fields.Many2one(
        'account.account',
        string=_('Default Account Purchase Price Difference'),
    )

    def get_default_account_product_price(self, cr, uid, ids, context=None):
        return {'purchase_price_account_id':
                self.pool['ir.values'].get_default(
                    cr, uid, 'purchase.config.settings',
                    'purchase_price_account_id')}

    def set_default_account_product_price(self, cr, uid, ids, context=None):
        config_value = self.browse(
            cr, uid, ids, context=context).purchase_price_account_id.id
        self.pool['ir.values'].set_default(cr, uid, 'purchase.config.settings',
                                           'purchase_price_account_id',
                                           config_value)
