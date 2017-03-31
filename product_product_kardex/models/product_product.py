# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

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

    @api.multi
    def print_kardex(self):
        return {
            'name': 'Product Kardex Report',
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
        }

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
