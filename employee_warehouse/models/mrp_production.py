# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model
    def action_produce(self, production_id, production_qty,
                       production_mode, wiz=False):
        produce_obj = self.env['mrp.production'].browse(production_id)
        for production in produce_obj:
            warehouse = production.location_dest_id.stock_warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        return super(MrpProduction, self).action_produce(
            production_id, production_qty, production_mode, wiz)
