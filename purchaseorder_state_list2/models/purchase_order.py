# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
'''import ipdb'''


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state_hist_ids = fields.One2many(
        'purchase.order.state.hist',
        'purchase_id',
        string='Purchase',
    )
    ''' Cada vez que una orden de presupuesto de cree registara la fecha
    en que fue creada y el estatus sera draft - no_review'''
    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)

        hist_obj = self.env['purchase.order.state.hist']
        his_vals = {
            'purchase_id': res.id,
            'date': fields.Datetime.now(),
            'status_new': res.state + "-" + res.review
        }
        hist_obj.create(his_vals)
        return res

    @api.multi
    def write(self, vals):
        newstate = ''
        hist_obj = self.env['purchase.order.state.hist']
        if('state' in vals.keys() or 'review' in vals.keys()):
            if('state' in vals.keys()):
                newstate = vals['state']
            else:
                newstate = self.state
            if('review' in vals.keys()):
                newstate += '-' + vals['review']
            else:
                newstate += '-' + self.review

            his_vals = {
                'purchase_id': self.id,
                'date': fields.Datetime.now(),
                'status_old': self.state + "-" + self.review,
                'status_new': newstate,
            }

            hist_obj.create(his_vals)
        return super(PurchaseOrder, self).write(vals)
