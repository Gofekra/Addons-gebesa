# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):

        res = super(SaleOrder, self).action_invoice_create(
            grouped, final)
        invoice = self.env['account.invoice'].browse(res)
        for inv in invoice:
            if inv.partner_id.parent_id:
                inv.sales_channel_id = \
                    inv.partner_id.parent_id.sales_channel_id
            else:
                inv.sales_channel_id = inv.partner_id.sales_channel_id
        return res


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        for inv in res:
            if inv.partner_id.parent_id:
                inv.sales_channel_id = \
                    inv.partner_id.parent_id.sales_channel_id
            else:
                inv.sales_channel_id = inv.partner_id.sales_channel_id
        return res
