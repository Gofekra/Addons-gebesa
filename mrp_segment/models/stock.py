# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )
