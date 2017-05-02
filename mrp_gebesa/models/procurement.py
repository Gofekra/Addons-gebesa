# -*- coding: utf-8 -*-
# © 2017 Cesar Barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models
from openerp.exceptions import UserError, ValidationError


class ProcurementOrder(models.Model):
    _name = "procurement.order"
    _inherit = "procurement.order"

    @api.multi
    def make_mo(self):
        """ So some validations about BOM
        """
        res = {}
        for procurement in self:
            properties = [x.id for x in procurement.property_ids]
            bom_id = self.env['mrp.bom']._bom_find(
                product_id=procurement.product_id.id,
                properties=properties, context=self._context)

            bombrw = self.env['mrp.bom'].browse(bom_id)
            if bombrw:
                cost_tot_bom = 0.000000
                for bomline in bombrw.bom_line_ids:
                    cost_tot_bom += (bomline.product_id.standard_price * bomline.product_qty)
                diff = procurement.product_id.standard_price - cost_tot_bom
                if abs(diff) > 0.6000:
                    raise UserError(_('The total cost of this BoM: %s is Not Equal to its Product cost!') % procurement.product_id.default_code)
                    return False

                if bombrw.type == 'normal' and not bombrw.routing_id:
                    raise UserError(_('This BoM: %s  is for Manufacturing, but has not a Production Route!') % procurement.product_id.default_code)
                    return False

                if bombrw.type == 'phantom' and bombrw.routing_id:
                    raise UserError(_('This BoM: %s  is a Kit, but it has a Production Route!') % procurement.product_id.default_code)
                    return False

        res = super(ProcurementOrder, self).make_mo()
        return res
