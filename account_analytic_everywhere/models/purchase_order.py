# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        related='picking_type_id.warehouse_id.account_analytic_id',
        string=_(u'Analytic Account'),
        store=True,
    )
