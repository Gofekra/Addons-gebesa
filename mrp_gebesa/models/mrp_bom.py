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

    @api.multi
    def write(self, values):
        # te traes el producto anterior
        # val = self.product_tmpl_id

        if 'product_tmpl_id' in values.keys():
            # te traes el objeto vacio
            template = self.env['product.template']
            # se construye el objeto, y los busca por medio del values
            val = template.browse(values['product_tmpl_id'])
            # condicion para la busquedan
            for route in val.route_ids:
                # Se le agrega el id como busqueda, cambia bd cambiarlo
                if route.id == 6:
                    raise UserError(_('This product is raw material'))
        return super(MrpBom, self).write(values)

    @api.model
    def create(self, vals):
        template = self.env['product.template']
        val = template.browse(vals['product_tmpl_id'])
        for route in val.route_ids:
            if route.id == 6:
                raise UserError(_('This product is raw material'))
        return super(MrpBom, self).create(vals)


class MrpBomLine(models.Model):
    _name = "mrp.bom.line"
    _inherit = "mrp.bom.line"

    location_id = fields.Many2one(
        'stock.location',
        string=_('Location'),
        required=True)

    @api.model
    def create(self, values):
        bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        if 'bom_id' in values.keys():
            bom = bom_obj.browse([values['bom_id']])
            product = product_obj.browse([values['product_id']])
            if bom.type == 'phantom':
                product_bom = bom_obj.search([
                    ('product_id', '=', values['product_id'])])
                if not product_bom:
                    raise UserError(_('You can not add a product that \
                        has no BOM: %s') % (product.name,))
            if product.standard_price == 0:
                raise UserError(_('You can not add a product with cost 0: %s')
                                % (product.name,))
        return super(MrpBomLine, self).create(values)
