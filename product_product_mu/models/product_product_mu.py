# -*- coding: utf-8 -*-
# © 2017 Aldo Nerio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ProductProductMu(models.Model):
    _name = 'product.product.mu'
    _description = 'Type move of product'
    _order = 'code asc'
    _rec_name = 'code'

    code = fields.Char(
        string=_(u'Code'), size=4,
        help=_(u'Code'),
    )
    mu_dist = fields.Float(
        string=_(u'M.U.Dist'),
        help=_(u'Process Dist')
    )
    mu_may = fields.Float(
        string=(u'M.U.May'),
        help=_(u'Process may')
    )
    limit_mu = fields.Float(
        string=(u'limit.Mu'),
        help=_(u'Limit')
    )
    company_id = fields.Many2one(
        'res.company', string=_(u'Company'),
        help=_(u'Company')
    )
