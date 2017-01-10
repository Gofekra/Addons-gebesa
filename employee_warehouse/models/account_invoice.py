# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            warehouse = invoice.account_analytic_id.warehouse_id
            employee = self.env['hr.employee'].search(
                [('user_id', '=', self._uid)])
            if warehouse not in employee.warehouse_ids:
                raise ValidationError(_("You do not have privileges to validate \
                                      in this warehouse."))
        return super(AccountInvoice, self).invoice_validate()
