# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'

    netsuite_line = fields.Integer(
        _('Line NS'),
        help=_('Line number on Netsuite'),
    )
