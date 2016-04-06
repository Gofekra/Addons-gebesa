# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    parent_id = fields.Many2one(
        'account.account',
        string=_(u'Parent'),
        help=_(u'Account parent'),
    )
