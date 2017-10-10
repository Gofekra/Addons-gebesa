# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    purchase_id = fields.Many2one(
        'purchase.order',
        string=_('Purchase Order'),
        readonly=True,
        # store=True,
        related='move_lines.purchase_line_id.order_id'
    )
