# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    account_id = fields.Many2one(
        'account.account',
        string=_(u'Inventory account'),
    )
