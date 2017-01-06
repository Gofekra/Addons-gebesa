# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):
        for picking in self:
            if picking.location_dest_id.usage in ('customer', 'transit'):
                warehouse = picking.location_id.stock_warehouse_id
            else:
                warehouse = picking.location_dest_id.stock_warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        super(StockPicking, self).do_new_transfer()
