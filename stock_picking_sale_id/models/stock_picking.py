# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order',
                              string=_(u'Sale Order'),
                              store=True,)
    cust_ven_id = fields.Many2one(
        related='sale_id.partner_id',
        string='Customer',
        store=True,
    )
    client_order_ref = fields.Char(
        related='sale_id.client_order_ref',
        string='Customer ref',
        store=True,
    )
