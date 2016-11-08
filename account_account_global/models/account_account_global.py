# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountAccountGlobal(models.Model):
    _name = 'account.account.global'
    _description = 'Account account global'

    module = fields.Char(
        string=_('Module'),
    )
    code = fields.Integer(
        string=_('Code'),
    )
    name = fields.Char(
        string=_('Name'),
    )
    account_id = fields.Many2one(
        'account.account',
        string=_('Account'),
    )

    _sql_constraints = [
        ('code_name_uniq', 'unique (code,name)',
         _('The code combination and name must be unique.')),
    ]
