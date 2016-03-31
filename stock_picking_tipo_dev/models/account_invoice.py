# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    dev_tipo = fields.Selection(
        [('normal', _(u'Normal')),
         ('rebilling', _(u'Rebilling')),
         ('cancellation', _(u'Cancellation'))],
        string=_(u"Type"),
        help=_("defines the type")
    )
