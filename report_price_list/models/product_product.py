# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_line = fields.Boolean(
        string=_('Is Line'),
        help=_('Indicates whether the Product is line'),
    )
