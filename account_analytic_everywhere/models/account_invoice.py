# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u'Analytic Account'),
    )
