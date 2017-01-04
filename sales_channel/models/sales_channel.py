# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class SalesChannel(models.Model):
    _name = 'sales.channel'
    _description = 'Sales channel for invoices'

    name = fields.Char(
        string=_('Name'),
        size=64,
    )

    code = fields.Char(
        string=_('code'),
        size=10,
    )

    description = fields.Text(
        string=_('Description'),
    )

    parent_id = fields.Many2one(
        'sales.channel',
        string=_('Parent'),
    )

    other_income = fields.Boolean(
        string=_('Other income'),
    )
    is_export = fields.Boolean(
        string='It is export',
    )
