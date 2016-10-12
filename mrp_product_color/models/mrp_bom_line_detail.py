# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class MrpBomLineDetail(models.Model):
    _inherit = 'mrp.bom.line.detail'

    color_id = fields.Many2one(
        'mrp.product.color',
        string=_('Color'),
    )
