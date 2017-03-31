# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class ProductProductKardex(models.Model):
    _name = 'product.product.kardex.wizard'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
    )
    location_id = fields.Many2one(
        'stock.location',
        string=_('Location'),
    )
    fecha_inicial = fields.Date(
        string=_('Date Init'),
    )
    fecha_final = fields.Date(
        string=_('Date End'),
    )
    # active_id = self._context.get('active_ids')

    @api.multi
    def print_report(self):
        ids = [self.id]
        ctx = dict(self.env.context or {},
                   active_ids=ids,
                   active_model=self._name)
        return{
            'type': 'ir.actions.report.xml',
            'report_name': 'product_kardex_report',
            'context': ctx,
        }
