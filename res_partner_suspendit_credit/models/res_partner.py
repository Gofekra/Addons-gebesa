# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_suspended = fields.Boolean(
        string=_('Suspended Credit'),
    )
