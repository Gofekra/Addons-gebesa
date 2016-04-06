# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def invoice_line_move_line_get(self):
        deposit_product_id = self.env['ir.values'].get_default(
            'sale.config.settings', 'deposit_product_id_setting')
        res = []
        for line in self.invoice_line_ids:
            if deposit_product_id == line.product_id.id:
                res = super(AccountInvoice, self).invoice_line_move_line_get()
            else:
                tax_ids = []
                for tax in line.invoice_line_tax_ids:
                    tax_ids.append((4, tax.id, None))
                    for child in tax.children_tax_ids:
                        if child.type_tax_use != 'none':
                            tax_ids.append((4, child.id, None))

                freight_account_id = self.env['ir.values'].get_default(
                    'account.config.settings', 'freight_account_id')
                installation_account_id = self.env['ir.values'].get_default(
                    'account.config.settings', 'installation_account_id')

                if not freight_account_id:
                    raise ValidationError(_(u"Please specify an account of \
                                          freight in Accounting --> \
                                          Configuration --> Settings"))
                if not installation_account_id:
                    raise ValidationError(_(u"Please specify an account of \
                                          installation in Accounting --> \
                                          Configuration --> Settings"))

                sale = line.price_subtotal
                total_freight = sale * (self.perc_freight / 100)
                sale = sale - total_freight
                total_installation = sale * (self.perc_installation / 100)
                sale = sale - total_installation

                amount = sale + total_installation + total_freight
                if (line.price_subtotal - amount) != 0:
                    sale = sale + (line.price_subtotal - amount)

                move_line_dict = {
                    'invl_id': line.id,
                    'type': 'src',
                    'name': line.name.split('\n')[0][:64],
                    'price_unit': line.price_unit,
                    'quantity': line.quantity,
                    'price': sale,
                    'account_id': line.account_id.id,
                    'product_id': line.product_id.id,
                    'uom_id': line.uom_id.id,
                    'account_analytic_id': line.account_analytic_id.id,
                    'tax_ids': tax_ids,
                    'invoice_id': self.id,
                }
                if self.perc_freight > 0.0:
                    move_line_freight_dict = {
                        'invl_id': line.id,
                        'type': 'src',
                        'name': line.name.split('\n')[0][:64],
                        'price': total_freight,
                        'account_id': freight_account_id,
                        'account_analytic_id': line.account_analytic_id.id,
                        'tax_ids': tax_ids,
                        'invoice_id': self.id,
                    }
                if self.perc_installation > 0.0:
                    move_line_installation_dict = {
                        'invl_id': line.id,
                        'type': 'src',
                        'name': line.name.split('\n')[0][:64],
                        'price': total_installation,
                        'account_id': installation_account_id,
                        'account_analytic_id': line.account_analytic_id.id,
                        'tax_ids': tax_ids,
                        'invoice_id': self.id,
                    }

                if line['account_analytic_id']:
                    move_line_dict['analytic_line_ids'] = [(
                        0, 0, line._get_analytic_line())]
                    if self.perc_freight > 0.0:
                        move_line_freight_dict['analytic_line_ids'] = [(
                            0, 0, line._get_analytic_line())]
                    if self.perc_installation > 0.0:
                        move_line_installation_dict['analytic_line_ids'] = [(
                            0, 0, line._get_analytic_line())]

                res.append(move_line_dict)
                if self.perc_freight > 0.0:
                    res.append(move_line_freight_dict)
                if self.perc_installation > 0.0:
                    res.append(move_line_installation_dict)
        return res
