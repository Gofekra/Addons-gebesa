# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    notify_approval = fields.Char(
        string=_('Notify Sale Approval'),
    )
