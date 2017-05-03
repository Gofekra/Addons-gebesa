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
    def unlink(self):
        for bom in self:
            if bom.bom_line_ids:
                raise UserError(_('This BOM has detail'))
        return super(MrpBom, self).unlink()

    @api.multi
    def write(self, values):
        # te traes el producto anterior
        # val = self.product_tmpl_id
        if 'type' in values.keys():
            types = values['type']
        else:
            types = self.type
        if 'warehouse_id' in values.keys():
            ware_obj = self.env['stock.warehouse']
            ware = ware_obj.browse(values['warehouse_id'])
        else:
            ware = self.warehouse_id
        if 'routing_id' in values.keys():
            routing_obj = self.env['mrp.routing']
            routing = routing_obj.browse(values['routing_id'])
        else:
            routing = self.routing_id
        if types == 'normal':
            if ware.id != routing.location_id.stock_warehouse_id.id:
                raise UserError(_('The production route must'
                                  ' be in the same warehouse than the bom'))
        if types == 'phantom':
            if routing.id != 0:
                raise UserError(_('Kit products should not have route production'))

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
        else:
            val = self.product_tmpl_id

        if 'product_id' in values.keys():
            producto_obj = self.env['product.product']
            product = producto_obj.browse(values['product_id'])

        else:
            product = self.product_id

        if val.id != product.product_tmpl_id.id:
            raise UserError(_('Product and template it does not match'))
        return super(MrpBom, self).write(values)

    @api.model
    def create(self, vals):
        # objeto para no guardar variantes ya existentes
        # bom_obj = self.env['mrp.bom']
        ware_obj = self.env['stock.warehouse']
        routing_obj = self.env['mrp.routing']
        producto_obj = self.env['product.product']
        template = self.env['product.template']
        val = template.browse(vals['product_tmpl_id'])
        ware = ware_obj.browse(vals['warehouse_id'])
        routing = routing_obj.browse(vals['routing_id'])
        if 'product_id' in vals.keys():
            product = producto_obj.browse(vals['product_id'])
            if val.id != product.product_tmpl_id.id:
                raise UserError(_('Product and template it does not match'))
        # objeto de busqueda para ver si ya existe
        # bom_id = bom_obj.search([('product_id', "=", vals['product_id']),
        #                         ('active', '=', True)])
        # if len(bom_id) > 0:
        #    raise UserError(_('This product is already exists'))
        if vals['type'] == 'normal':
            if ware.id != routing.location_id.stock_warehouse_id.id:
                raise UserError(_('The production route must'
                                  'be in the same warehouse than the bom'))
        if vals['type'] == 'phantom':
            if routing.id != 0:
                raise UserError(_('Kit products should not have route production'))
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
            # Comentariado temporalmente para subir detalles restantes
                # if not product_bom:
                #     raise UserError(_('You can not add a product that \
                #         has no BOM: %s') % (product.name,))
            
            #if product.standard_price == 0:
            #    raise UserError(_('You can not add a product with cost 0: %s')
            #                    % (product.name,))
        return super(MrpBomLine, self).create(values)

    # temporary
    @api.multi
    def write(self, values):
        if 'bom_id' in values.keys() and self._uid in (1, 37, 38, 86, 107):
            return
        return super(MrpBomLine, self).write(values)
