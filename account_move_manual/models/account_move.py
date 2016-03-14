# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    manual = fields.Boolean(
        string=_(u'Manual'),
        help=_(u'It indicates whether the movement was created manually')
    )

    user = fields.Char(
        string=_(u'User'),
        help=_(u'It indicates the user who created the policy'),
        default=lambda self: self.env['res.users'].browse(self._uid).name
    )

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        self.manual = False
        if self.journal_id:
            self.manual = True
