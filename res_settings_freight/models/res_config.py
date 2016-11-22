# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp import SUPERUSER_ID


class SaleConfiguration(models.TransientModel):
    _inherit = 'account.config.settings'

    freight_account_id = fields.Many2one(
        'account.account',
        string=_(u'Default account freight'),
    )

    installation_account_id = fields.Many2one(
        'account.account',
        string=_(u'Default account installation'),
    )

    return_account_id = fields.Many2one(
        'account.account',
        string=_(u'Default account sales return'),
    )

    @api.v7
    def set_freight_account_id_defaults(self, cr, uid, ids, context=None):
        freight_account_id = self.browse(
            cr, uid, ids, context=context).freight_account_id
        res = self.pool.get('ir.values').set_default(
            cr, SUPERUSER_ID, 'account.config.settings',
            'freight_account_id', freight_account_id.id)
        return res

    @api.v7
    def set_installation_account_id_defaults(self, cr, uid, ids, context=None):
        installation_account_id = self.browse(
            cr, uid, ids, context=context).installation_account_id
        res = self.pool.get('ir.values').set_default(
            cr, SUPERUSER_ID, 'account.config.settings',
            'installation_account_id', installation_account_id.id)
        return res

    @api.v7
    def set_return_account_id_defaults(self, cr, uid, ids, context=None):
        return_account_id = self.browse(
            cr, uid, ids, context=context).return_account_id
        res = self.pool.get('ir.values').set_default(
            cr, SUPERUSER_ID, 'account.config.settings',
            'return_account_id', return_account_id.id)
        return res
