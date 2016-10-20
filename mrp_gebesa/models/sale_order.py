# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    production_status = fields.Selection(
        [('no_production', _('No Production')),
         ('partial_production', _('Partial Production')),
         ('total_production', _('Total Production'))],
        string=_("Production Status"),
        default='no_production',
    )
