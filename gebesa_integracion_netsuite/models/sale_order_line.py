# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_order_line_invoice_line(
            self, cr, uid, line, account_id=False, context=None):
        res = super(SaleOrderLine, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id, context=context)
        res.update(netsuite_line=line.netsuite_line)

        return res
