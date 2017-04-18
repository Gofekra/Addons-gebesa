# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models, api
from openerp.exceptions import UserError


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    bom_line_detail_ids = fields.One2many(
        'mrp.bom.line.detail',
        'bom_line_id',
        string=_('BoM Line Details'),
        copy=True,
    )

    @api.multi
    def write(self, values):
        if 'product_id' in values.keys():
            bom_obj = self.env['mrp.bom']
            product_obj = self.env['product.product']
            producto = product_obj.browse(values['product_id'])
            bom = bom_obj.browse(values['bom_id'])
            if producto.id == bom.product_id.id:
                raise UserError(_('One product cannot be detail of itself'))
            for line in bom.bom_line_ids:
                if line.product_id.id == producto.id:
                    raise UserError(_('This product is already in this Bom'))
        return super(MrpBomLine, self).write(values)

    @api.multi
    def create(self, vals):
        bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        producto = product_obj.browse(vals['product_id'])
        bom = bom_obj.browse(vals['bom_id'])
        if producto.id == bom.product_id.id:
            raise UserError(_('One product cannot be detail of itself'))
        for line in bom.bom_line_ids:
            if line.product_id.id == producto.id:
                raise UserError(_('This product is already in this Bom'))
        return super(MrpBomLine, self).create(vals)
