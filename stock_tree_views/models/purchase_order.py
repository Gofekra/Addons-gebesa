# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        # related='picking_type_id.warehouse_id',
        string=_('Warehouse'),
        compute='_compute_warehouse_id',
        store=True,
    )

    @api.depends('picking_type_id')
    def _compute_warehouse_id(self):
        super(PurchaseOrder, self)._onchange_picking_type_id()
        warehouse = self.picking_type_id.warehouse_id
        self.warehouse_id = warehouse.id
