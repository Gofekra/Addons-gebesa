# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sales_channel_id = fields.Many2one(
        'sales.channel',
        string=_('Sales channel'),
    )
