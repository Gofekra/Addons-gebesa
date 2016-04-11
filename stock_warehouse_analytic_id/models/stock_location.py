# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class StockLocation(models.Model):
    _inherit = 'stock.location'

    stock_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_('Stock Warehouse'),
    )
