# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        self.ensure_one()

        res = super(SaleOrderLine, self)._prepare_order_line_procurement(
            group_id)
        # res.update({'account_analytic_id': self.order_id.project_id.id})
        return res
