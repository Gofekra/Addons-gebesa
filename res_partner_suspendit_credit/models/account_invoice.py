# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        for inv in self:
            if inv.type == 'out_invoice':
                if inv.partner_id.commercial_partner_id and\
                   inv.partner_id.commercial_partner_id.is_suspended:
                    raise UserError(
                        _('You can not bill !'
                          ' The Client has suspended your credit,'
                          ' contact the Department of'
                          ' Credit and Collections.'))

                if inv.partner_id and inv.partner_id.is_suspended:
                    raise UserError(
                        _('You can not bill !'
                          ' The Client has suspended your credit,'
                          ' contact the Department of'
                          ' Credit and Collections.'))

            return super(AccountInvoice, self).action_move_create()
