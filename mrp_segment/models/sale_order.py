# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    segment_status = fields.Selection(
        [('no_segment', _('No Segment')),
         ('partial_segment', _('Partial Segment')),
         ('total_segment', _('Total Segment'))],
        string=_("Segment Status"),
        default='no_segment',
    )
