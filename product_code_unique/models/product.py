# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    _sql_constraints = [
        ('default_uniq', 'unique (default_code)',
         _('The field Internal Reference must be unique!'))
    ]
