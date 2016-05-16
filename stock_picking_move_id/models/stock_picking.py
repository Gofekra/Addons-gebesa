# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    am_ids = fields.Many2many('account.move',
                              string=_('Account Entries'),
                              ondelete='set null',
                              select=True)
