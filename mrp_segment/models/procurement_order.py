# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )
