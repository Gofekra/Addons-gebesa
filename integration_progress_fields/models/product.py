# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models, fields


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    numctrl_progress = fields.Integer(
        _('Num. Ctrl. Progress'),
    )

    _sql_constraints = [
        ('default_uniq', 'unique (default_code)',
         _('The field Num. Ctrl. Progress must be unique!'))
    ]
