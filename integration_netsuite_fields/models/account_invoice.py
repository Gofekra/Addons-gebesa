# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    msj = fields.Text(
        string=_('Last Message'),
        readonly=True,
        track_visibility='onchange',
        help=_('Message generated to upload XML to sign'),
    )

    netsuite_ok = fields.Boolean(
        string=_('Netsuite Updated'),
        help=_('It indicates whether update the order status in NetSuite'),
        readonly=True,
        store=True,
    )


class AccountInvoiceLine(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    netsuite_line = fields.Integer(
        _('Line NS'),
        help='Line number on Netsuite',
    )
