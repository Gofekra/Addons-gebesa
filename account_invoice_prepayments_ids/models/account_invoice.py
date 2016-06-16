# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    prepayment_number = fields.Text(
        string=_('Number Invoice Advance'),
    )

    prepayment_move_ids = fields.Many2many(
        'account.move',
        string=_('Accountant Move of the Advance Invoice'),
    )

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        lines_fac = []
        resul = []
        resp = []
        for line in self.invoice_line_ids:
            lines_fac = line.sale_line_ids.invoice_lines
            for fact in lines_fac:
                deposit = self.pool['ir.values'].get_default(
                    self._cr, self._uid, 'sale.config.settings',
                    'deposit_product_id_setting') or False
                if line.product_id.id == deposit and fact.id != line.id:
                    resul.append(str(fact.invoice_id.number))
                    self.prepayment_number = resul
                    resp.append(fact.invoice_id.move_id.id)
                    self.prepayment_move_ids = resp

        return res
