# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError


class AccountRegisterPaymentsLine(models.Model):
    _inherit = 'account.register.payments.line'

    factoring_number = fields.Char(
        string=_("Factoring Number"),
        readonly=True)

class AccountRegisterPayments(models.Model):
    _inherit = 'account.register.payments'

    @api.model
    def default_get(self, fields):
        rec = super(AccountRegisterPayments, self).default_get(fields)
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')

        # Checks on context parameters
        if not active_model or not active_ids:
            raise UserError(_(u"Programmation error: \
                            wizard action executed without active_model \
                            or active_ids in context."))
        if active_model != 'account.invoice':
            raise UserError(_(u"Programmation error: the expected model \
                            for this action is 'account.invoice'. \
                            The provided one is '%d'.") % active_model)

        # Checks on received invoice records
        invoices = self.env[active_model].browse(active_ids)
        lines = []
        aml_ids = False
        account_type = False
        if any(invoice.type == 'out_invoice' for invoice in invoices):
            account_type = 'receivable'
        elif any(invoice.type == 'in_invoice' for invoice in invoices):
            account_type = 'payable'

        # if any(invoice.type == 'out_invoice' and
        #        invoice.factoring_customer_id for invoice in invoices):
        #     raise UserError(_("Some (s) of this Invoice (s) are contemplated"
        #                       " in Factoring. Please check!"))

        # Fill the defaults values of the selected invoices
        for inv in invoices:
            aml_ids = self.env[
                'account.move.line'].search([
                                            ('account_id.internal_type', '=',
                                             account_type),
                                            ('full_reconcile_id', '=', False),
                                            ('move_id', '=', inv.move_id.id)],
                                            limit=1,
                                            order='date_maturity')
            account_id = aml_ids[0].account_id.id
            analytic_id = aml_ids[0].analytic_account_id.id
            aprl = {
                'move_line_id': aml_ids[0].id,
                'account_id': account_id,
                'untax_amount': inv.amount_untaxed,
                'amount': inv.residual,
                'name': inv.name,
                'origin': inv.origin,
                'reference': inv.reference,
                'reconcile': True,
                'account_analytic_id': analytic_id,
                'date_original': inv.date_invoice,
                'partner_id': inv.partner_id.id,
                'date_due': inv.date_due,
                'company_id': inv.company_id.id,
                'amount_original': inv.amount_total,
                'amount_unreconciled': inv.residual,
                'currency_id': inv.currency_id.id,
                'invoice_id': inv.id,
                'register_payment_id': self.id,
                'factoring_number': inv.factoring_customer_id.consecutive or
                inv.factoring_supplier_id.consecutive,
            }
            lines.append([0, False, aprl])
        rec.update({
            'line_ids': lines,
        })
        return rec
