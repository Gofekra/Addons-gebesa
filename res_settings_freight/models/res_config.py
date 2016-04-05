# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    freight_account_id = fields.Many2one(
        'account.account',
        string=_(u'Default account freight'),
    )

    installation_account_id = fields.Many2one(
        'account.account',
        string=_(u'Default account installation'),
    )
