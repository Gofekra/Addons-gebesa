# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    stock_move_type_id = fields.Many2one(
        'stock.move.type',
        string=_(u'Type of move'),
    )
