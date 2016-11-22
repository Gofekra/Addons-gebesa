# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_line = fields.Boolean(
        string=_('Line Product'),
        default=False,
    )

    family_id = fields.Many2one(
        'product.family',
        string=_('Family'),
    )

    group_id = fields.Many2one(
        'product.group',
        string=_('Group'),
    )

    line_id = fields.Many2one(
        'product.line',
        string=_('Line'),
    )

    type_id = fields.Many2one(
        'product.type',
        string=_('Type'),
    )
