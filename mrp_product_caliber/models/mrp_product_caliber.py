# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, models, fields
from openerp.addons import decimal_precision as dp


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

    espesor_mm = fields.Float(
        string=_('Density MM'),
        digits_compute=dp.get_precision('Product Unit of Measure'),
    )

    espesor_pgs = fields.Float(
        string=_('Density PGS'),
        digits_compute=dp.get_precision('Product Unit of Measure'),
    )

    peso_kg = fields.Float(
        string=_('Weight KG'),
        digits_compute=dp.get_precision('Product Unit of Measure'),
    )

    peso_lb = fields.Float(
        string=_('Weight LB'),
        digits_compute=dp.get_precision('Product Unit of Measure'),
    )

    _sql_constraints = [
        ('default_uniq', 'unique (key_caliber)',
         _('The field Key Caliber must be unique!'))
    ]
