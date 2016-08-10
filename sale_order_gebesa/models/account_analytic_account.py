# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    use_salesorder = fields.Boolean(
        string=_(u'Analytic available for sales order'),
        default=False,
    )

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_(u'Default warehouse'),
        help=_(u'Warehouse for the sales order'),
    )
