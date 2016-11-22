# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sales_channel_id = fields.Many2one(
        'sales.channel',
        string=_('Sales channel'),
    )

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        super(AccountInvoice, self)._onchange_partner_id()
        sales_channel_id = False
        if self.partner_id.sales_channel_id.id:
            sales_channel_id = self.partner_id.sales_channel_id.id
        self.sales_channel_id = sales_channel_id
