# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    bom_line_detail_ids = fields.One2many(
        'mrp.bom.line.detail',
        'bom_line_id',
        string=_('BoM Line Details'),
        copy=True,
    )
