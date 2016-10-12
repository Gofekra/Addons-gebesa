# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class MrpProductColor(models.Model):
    _name = 'mrp.product.color'
    _description = 'Product Color'

    code = fields.Char(
        string=_('Code'),
    )
    name = fields.Char(
        string=_('Name'),
    )
