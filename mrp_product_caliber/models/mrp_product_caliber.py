# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models, fields


class MrpProductCaliber(models.Model):
    _name = 'mrp.product.caliber'
    _description = "Calibers"
    _order = 'key_caliber asc'
    _rec_name = 'name_caliber'

    key_caliber = fields.Char(
        string=_('Key Caliber'),
    )

    name_caliber = fields.Char(
        string=_('Name Caliber'),
    )

    _sql_constraints = [
        ('default_uniq', 'unique (key_caliber)',
         _('The field Key Caliber must be unique!'))
    ]
