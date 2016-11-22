# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    advance_id = fields.Many2one(
        'account.invoice',
        string=_('Advance Invoice'),
    )

    amount_advance = fields.Float(
        _('Amount Advance'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_amount_adv',
        store=True,
    )

    @api.onchange('advance_id')
    def _onchange_advance_id(self):
        advance = self.advance_id
        if advance:
            amount = advance.amount_total
            self.amount_advance = amount
        else:
            self.amount_advance = 0.0

        return

    @api.depends('advance_id')
    def _compute_amount_adv(self):
        if self.advance_id:
            self.amount_advance = self.advance_id.amount_total

    @api.multi
    def action_move_create(self):
        for inv in self:
            if inv.advance_id and not inv.advance_id.sale_id:
                adv_id = inv.advance_id
                prod_adv = False
                tax_prod = []
                for line in adv_id.invoice_line_ids:
                    deposit = self.pool['ir.values'].get_default(
                        self._cr, self._uid, 'sale.config.settings',
                        'deposit_product_id_setting') or False
                    if line.product_id.id == deposit:
                        product = self.env['product.product'].search(
                            [('id', '=', deposit)])
                        prod_adv = product
                        tax_prod = [(6, 0, [x.id for x in
                                     line.product_id.taxes_id])]

                if not prod_adv:
                    raise UserError(_('The Advance Invoice to which it refers,'
                                      '\n does not have an Article type'
                                      'in Advance'))

                inv_line_values2 = {
                    'name': _('Aplication of advance'),
                    'origin': inv.advance_id.number,
                    'account_id': prod_adv.property_account_income_id.id,
                    'price_unit': inv.amount_advance * -1,
                    'quantity': 1.0,
                    'discount': False,
                    'uom_id': prod_adv.uom_id.id or False,
                    'product_id': prod_adv.id,
                    'invoice_line_tax_id': tax_prod,
                    'account_analytic_id': inv.account_analytic_id.id,
                    'invoice_id': inv.id,
                }
                inv_line_obj = self.env['account.invoice.line']
                inv_line_id = inv_line_obj.create(inv_line_values2)

                inv.advance_id.advance_applied = True

        super(AccountInvoice, self).action_move_create()

        return True
