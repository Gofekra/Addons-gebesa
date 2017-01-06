# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.multi
    def prepare_inventory(self):
        for inventory in self:
            warehouse = inventory.location_id.stock_warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        super(StockInventory, self).prepare_inventory()

    @api.multi
    def action_done(self):
        for inventory in self:
            warehouse = inventory.location_id.stock_warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        super(StockInventory, self).action_done()
