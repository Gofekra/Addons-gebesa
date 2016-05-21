# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models


class MrpBomLineDetail(models.Model):
    _name = 'mrp.bom.line.detail'
    _order = "row"
    _rec_name = 'row'

    @api.model
    def _default_row(self):
        last_id = 0
        get_count = self.search_count([(1, '=', 1)])
        if get_count:
            last_id = get_count + 1
        else:
            last_id = 1
        row = str(last_id).rjust(5, '0')
        return row

    bom_line_id = fields.Many2one(
        'mrp.bom.line',
        string=_('Parent BoM Line'),
        ondelete='cascade',
        select=True,
        # required=True,
    )

    product_id = fields.Many2one(
        'product.product',
        string=_('Composite Article'),
        required=True,
    )

    row = fields.Char(
        _('Row'),
        default=_default_row,
        help=_('Gives the row order when displaying.'),
    )

    quantity = fields.Float(
        _('Quantity'),
    )

    width_cut = fields.Float(
        _('Cut Width'),
    )

    thickness = fields.Float(
        _('Thickness'),
    )

    material = fields.Char(
        string=_('Material'),
    )

    meters2 = fields.Float(
        _('Meters2'),
    )

    # color_id = fields.Many2one(
    #     'product.attribute.value',
    #     string=_('Color'),
    # )

    # caliber_id = fields.Many2one(
    #     'product.attribute.value',
    #     string=_('Caliber'),
    # )

    long_cut = fields.Float(
        _('Cut Long'),
    )

    side = fields.Integer(
        _('Sides'),
    )

    kilos = fields.Float(
        _('Kilos'),
    )

    variants = fields.Char(
        string='Filed Label',
    )

    _sql_constraints = [
        ('row_uniq', 'unique (row)',
         _('The row must be unique !')),
    ]
