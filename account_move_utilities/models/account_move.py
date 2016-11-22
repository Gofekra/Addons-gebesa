# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def delete_zeros(self):
        move_line_obj = self.env['account.move.line']

        self._cr.execute('UPDATE account_move '
                         'SET state=%s '
                         'WHERE id IN %s', ('draft', tuple([self._id]),))

        for move in self:
            for line in move.line_ids:
                debit = line.debit or False
                credit = line.credit or False

            if not debit and not credit:
                move_line_obj.unlink()

            self.post()

    def assigned_analytics(self, analytic_id=False):
        move_line_obj = self.env['account.move.line']

        self._cr.execute('UPDATE account_move '
                         'SET state=%s '
                         'WHERE id IN %s', ('draft', tuple([self._id]),))

        for move in self:
            resul = []
            for line in move.line_ids:
                analytic = line.analytic_account_id or False
                if not analytic:
                    resul.append(line.id)
            move_line_obj.write(resul, {'analytic_account_id': analytic_id})
            self.post()
