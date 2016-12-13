# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lines = fields.Char(
        string='Lines',
        compute='_compute_lines'
    )
    groups = fields.Char(
        'Groups',
        compute='_compute_lines'
    )
    familys = fields.Char(
        'Family',
        compute='_compute_lines'
    )
    volume = fields.Float(
        'Volumen',
        compute='_compute_lines'
    )
    weight = fields.Float(
        'Weight',
        compute='_compute_lines'
    )
    delay = fields.Integer(
        'Delay',
        compute='_compute_delay'
    )

    @api.depends('date_order')
    def _compute_delay(self):
        for sale in self:
            delay = datetime.strptime(fields.Date.today(), "%Y-%m-%d") -\
                datetime.strptime(sale.date_order[:10], "%Y-%m-%d")
            sale.delay = delay.days

    @api.depends('order_line')
    def _compute_lines(self):
        for sale in self:
            lin = grou = fam = ''
            volume = weight = 0
            lines = groups = family = []
            for order_line in sale.order_line:
                product = order_line.product_id
                volume += (order_line.product_uom_qty * product.volume)
                weight += (order_line.product_uom_qty * product.weight)
                if product.family_id.name not in family:
                    family.append(product.family_id.name)
                    fam = fam + ' ' + product.family_id.name + ','
                if product.group_id.name not in groups:
                    groups.append(product.group_id.name)
                    grou = grou + ' ' + product.group_id.name + ','
                if product.line_id.name not in lines:
                    lines.append(product.line_id.name)
                    lin = lin + ' ' + product.line_id.name + ','
            sale.lines = lin[1:-1]
            sale.groups = grou[1:-1]
            sale.familys = fam[1:-1]
            sale.volume = volume
            sale.weight = weight
