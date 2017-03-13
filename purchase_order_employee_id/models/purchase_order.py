# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    employee_id = fields.Many2one(
        'hr.employee',
        string=_('Employee'),
        store=True,
    )
