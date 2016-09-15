# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    aut_estatus_pago = fields.Selection(
        [('none', _('None')),
         ('proposed', _('Proposed')),
         ('authorized', _('Authorized')),
         ('rejected', _('Rejected'))],
        string=_("Payment authorization status"),
        default='none',
    )

    @api.multi
    def action_payment_auth_request(self):
        for invoice in self:
            invoice.aut_estatus_pago = 'proposed'
        return True

    @api.multi
    def action_payment_auth(self):
        for invoice in self:
            invoice.aut_estatus_pago = 'authorized'
        return True

    @api.multi
    def action_refuse_payment(self):
        for invoice in self:
            invoice.aut_estatus_pago = 'rejected'
        return True
