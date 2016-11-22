# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _default_get_price_account(self):
        res = self.env['ir.values'].get_default(
            'purchase.config.settings', 'purchase_price_account_id')
        return res

    property_account_creditor_price_difference = fields.Many2one(
        'account.account',
        string=_('Price Difference Account'),
        company_dependent=True,
        default=_default_get_price_account,
        help=_('This account will be used to value price difference'
               'between purchase price and cost price.')
    )

    def create(self, cr, uid, vals, context=None):
        product_template_id = super(ProductTemplate, self).create(
            cr, uid, vals, context=context)

        generate_account_price = self.pool['ir.values'].get_default(
            cr, uid, 'purchase.config.settings',
            'purchase_price_account_id')

        self.write(cr, uid, product_template_id,
                   {'property_account_creditor_price_difference':
                    generate_account_price}, context=None)

        return product_template_id
