# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist = fields.Boolean(
        string=_('Is price list'),
        help=_('the product is displayed in the price list'),
    )
    note_pricelist = fields.Text(
        string=_('Note price list'),
    )
    length = fields.Integer(
        string=_('Length'),
        help=_('length in cm'),
    )
    width = fields.Integer(
        string=_('Width'),
        help=_('width in cm'),
    )
    height = fields.Integer(
        string=_('Height'),
        help=_('height in cm'),
    )
    isometric = fields.Binary(
        string=_("Isometric image"),
        attachment=True,
    )
    isometric_medium = fields.Binary(
        string=_("Medium-sized isometric image"),
        compute='_compute_isometric',
        inverse='_inverse_medium_isometric',
        store=True,
        attachment=True,
    )
    isometric_small = fields.Binary(
        string=_("Small-sized isometric image"),
        compute='_compute_isometric',
        inverse='_inverse_small_isometric',
        store=True,
        attachment=True,
    )
    product_mix_id = fields.Many2one(
        'product.template',
        string='Product mixta',
    )
    vias = fields.Selection(
        [(2, 2),
         (3, 3),
         (4, 4)],
        string="Vias",
    )

    @api.depends('isometric')
    def _compute_isometric(self):
        for rec in self:
            rec.isometric_medium = tools.image_resize_image_medium(
                rec.isometric,
                avoid_if_small=True)
            rec.isometric_small = tools.image_resize_image_small(rec.isometric)

    def _inverse_medium_isometric(self):
        for rec in self:
            rec.isometric = tools.image_resize_image_big(rec.isometric_medium)

    def _inverse_small_isometric(self):
        for rec in self:
            rec.isometric = tools.image_resize_image_big(rec.isometric_small)


class ProductLine(models.Model):
    _inherit = 'product.line'

    acabados_html = fields.Html(
        string='Finished Html',
    )

    notas_html = fields.Html(
        string='Notes Html',
    )

    composiciones_html = fields.Html(
        string='Compositions Html',
    )


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    number = fields.Char(
        string='Number',
        compute='_compute_number'
    )

    @api.depends('attribute_code')
    def _compute_number(self):
        for record in self:
            record.number = "".join(
                [x for x in record.attribute_code if x.isdigit()])
