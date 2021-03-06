# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    included_id = fields.Many2one(
        'account.tax',
        string=_(u'Tax included'),
    )
