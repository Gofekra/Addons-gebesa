# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'product.group'
    _order = "name asc"

    name = fields.Char(
        string=_('Name'),
        size=120,
        required=True,
        help=_('Group name product'),
    )

    active = fields.Boolean(
        string=_('Active'),
        default=True
    )

    mu_min = fields.Float(
        string=_('M.U. Minimum')
    )
