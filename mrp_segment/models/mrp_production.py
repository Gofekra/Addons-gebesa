# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    segment_line_ids = fields.One2many(
        'mrp.segment.line',
        'mrp_production_id',
        string=_('Segment'),
    )
