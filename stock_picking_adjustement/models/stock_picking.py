# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    type_adjustment_id = fields.Many2one('type.adjustment',
                                         string=_('Type Adjustment'),
                                         store=True,)
