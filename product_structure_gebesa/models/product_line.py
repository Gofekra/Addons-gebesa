# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductLine(models.Model):
    _name = 'product.line'
    _description = 'product.line'
    _order = "name asc"

    code = fields.Char(
        string=_('Code'),
        size=5,
        required=True,
        help=_('Line code product'),
    )

    name = fields.Char(
        string=_('Name'),
        size=120,
        required=True,
        help=_('Line name product'),
    )

    product_family_id = fields.Many2one(
        'product.family',
        string=_('Product Family'),
    )

    active = fields.Boolean(
        string=_('Active'),
        default=True
    )

    report_type = fields.Selection(
        [('normal', _('NORMAL')),
         ('modulares', _('MODULARES'))],
        string=_("Type Report"),
    )

    mu_min = fields.Float(
        string=_('M.U. Minimum')
    )
