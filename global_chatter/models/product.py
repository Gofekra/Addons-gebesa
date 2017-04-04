# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'message.post.show.all']


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'message.post.show.all']
