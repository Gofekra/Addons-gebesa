# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        # related='picking_type_id.warehouse_id.account_analytic_id',
        string=_(u'Analytic Account'),
        compute='_compute_account_analytic_id',
        store=True,
    )

    @api.depends('picking_type_id')
    def _compute_account_analytic_id(self):
        warehouse = self.picking_type_id.warehouse_id
        self.account_analytic_id = warehouse.account_analytic_id.id
