# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta
from openerp import _, api, models
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        """ Create the movements to the given date,
        according to the days of tolerance granted to the user"""
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self._uid)])
        if not employee:
            raise UserError(_('You do not have an assigned employee.\n Please \
                            contact your system administrator'))
        employee_days = employee[0].tolerance_days

        for inv in self:
            if inv.date_invoice is not False:
                days_tol = str(date.today() - timedelta(days=employee_days))
                if inv.date_invoice < days_tol:
                    raise UserError(_('You can not bill! \
                                    The date may not be earlier \
                                    than %s .') % days_tol)

        return super(AccountInvoice, self).action_move_create()
