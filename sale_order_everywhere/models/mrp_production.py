# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale order',
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        copy=False,
    )
    client_order_ref = fields.Char(
        string='Customer ref',
        copy=False,
    )
    city_shipping = fields.Char(
        string='City',
        copy=False,
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
    )
