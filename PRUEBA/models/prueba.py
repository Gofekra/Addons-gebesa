# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class Prueba(models.Model):
    _name = 'prueba'
    _description = 'prueba'

    origin = fields.Char(
        string=_('Origin'),
    )
    date = fields.Integer(
        string=_('Date'),
    )
    name = fields.Char(
        string=_('Name'),
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=_('Account'),
    )

    _sql_constraints = [
        ('code_name_uniq', 'unique (code,name)',
         _('The code combination and name must be unique.')),
    ]
