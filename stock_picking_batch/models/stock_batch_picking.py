# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockBatchPicking(models.Model):
    _inherit = 'stock.batch.picking'

    @api.multi
    def action_assign(self):
        """ Check if batches pickings are available.
        """
        batches = self.get_not_empties()
        batches.mapped('active_picking_ids').force_assign()
