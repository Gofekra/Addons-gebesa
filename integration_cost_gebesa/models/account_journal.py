# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    integration_cost = fields.Boolean(
        string=_('Is integration cost'),
    )
