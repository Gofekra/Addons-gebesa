# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist = fields.Boolean(
        string=_('Price list'),
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


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    line_id = fields.Many2one('product.line',
                              string='Product line',)
    target_id = fields.Many2one('product.attribute.target',
                                ondelete='restrict',
                                string="Apply to",
                                store=True)
    attribute_id = fields.Many2one('product.attribute',
                                   string='Attribute',)
    value_ids = fields.Many2many('product.attribute.value',
                                 id1='line_id',
                                 id2='val_id',
                                 string='Attribute Values',
                                 )


class ProductAttributeTarget(models.Model):
    _name = 'product.attribute.target'

    target_code = fields.Char(
        string=_('Code'),)

    target_name = fields.Char(
        string=_('Name'),)


class ProductLine(models.Model):
    _inherit = 'product.line'

    attribute_line_ids = fields.One2many(
        'product.attribute.line',
        'line_id',
        string='Product attribute',
    )
