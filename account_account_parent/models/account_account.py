# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'
    _name = 'account.account'

    @api.multi
    def _get_account_level(self, level):
        """
        get the account level in the whole account chart
        """
        self.ensure_one()
        level += 1

        if self.parent_id and self.parent_id.id:
            return self.parent_id._get_account_level(level)
        else:
            return level

    parent_id = fields.Many2one(
        'account.account',
        string=_(u'Parent'),
        help=_(u'Account parent'),
    )

    _sql_constraints = [
        ('id_parent_id',
         'CHECK(id != parent_id)',
         _("The account cannot be parent of itself")),
    ]
