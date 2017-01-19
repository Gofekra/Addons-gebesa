# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale order',
    )
    partner_id = fields.Many2one(
        related='sale_id.partner_id',
        string='Customer',
        store=True,
    )
    client_order_ref = fields.Char(
        related='sale_id.client_order_ref',
        string='Customer ref',
        store=True,
    )
