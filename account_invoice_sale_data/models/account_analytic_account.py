# -*- coding: utf-8 -*-
# © 2016 Cesar Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    journal_sale_id = fields.Many2one(
        'account.journal',
        string=_(u'Default sale journal'),
        help=_(u'Default sale journal for this analytic'),
    )
