# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class StockMoveType(models.Model):
    _name = 'stock.move.type'
    _description = 'Type move of stock'
    _order = 'name asc'
    _rec_name = 'name'

    code = fields.Char(
        string=_(u'Code'), size=5,
        help=_(u'Code'),
    )
    name = fields.Char(
        string=_(u'Name'), size=120,
        help=_(u'Process name')
    )
    type = fields.Selection(
        [('input', _(u'Input')),
         ('output', _(u'Output')),
         ('internal', _(u'Internal'))],
        string=_(u"Type of move"),
    )
    company_id = fields.Many2one(
        'res.company', string=_(u'Company'),
        help=_(u'Company')
    )
