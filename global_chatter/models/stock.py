# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'message.post.show.all']


class StockBatchPicking(models.Model):
    _name = 'stock.batch.picking'
    _inherit = ['stock.batch.picking', 'message.post.show.all']
