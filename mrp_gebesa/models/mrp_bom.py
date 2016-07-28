# -*- coding: utf-8 -*-
# © <2016> Cesar barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class MrpBom(models.Model):
    _name = "mrp.bom"
    _inherit = "mrp.bom"

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True)

class MrpBomLine(models.Model):
    _name = "mrp.bom.line"
    _inherit = "mrp.bom.line"

    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        required=True)

# class StockLocation(models.Model):
#     _name = "stock.location"
#     _inherit = "stock.location"

#     code = fields.Char(
#         string=_(u'code')
#     )
