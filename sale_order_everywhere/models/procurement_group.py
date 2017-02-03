# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale',
    )
