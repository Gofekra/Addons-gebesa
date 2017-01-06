# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def action_produce(self, production_qty,
                       production_mode, wiz=False):
        for production in self:
            warehouse = production.location_dest_id.stock_warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        super(MrpProduction, self).action_produce(
            production_qty, production_mode, wiz)
