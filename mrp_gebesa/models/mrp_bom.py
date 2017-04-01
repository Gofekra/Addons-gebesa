# -*- coding: utf-8 -*-
# © <2016> Cesar barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class MrpBom(models.Model):
    _name = "mrp.bom"
    _inherit = "mrp.bom"

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_('Warehouse'),
        required=True)


class MrpBomLine(models.Model):
    _name = "mrp.bom.line"
    _inherit = "mrp.bom.line"

    location_id = fields.Many2one(
        'stock.location',
        string=_('Location'),
        required=True)

    # @api.model
    # def create(self, values):
    #     bom_obj = self.env['mrp.bom']
    #     if 'bom_id' in values.keys():
    #         bom = bom_obj.browse([values['bom_id']])
    #         if bom.type == 'phantom':
    #             product_bom = bom_obj.search([
    #                 ('product_id', '=', values['product_id'])])
    #             if not product_bom:
    #                 raise UserError(_('You can not add a product that \
    #                     has no BOM'))
    #     return super(MrpBomLine, self).create(values)
