# -*- coding: utf-8 -*-
# © <2016> <Cesar Barron Bautista>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError


class AccountPayment(models.Model):
    _name = "account.payment"
    _inherit = "account.payment"
    _description = "Payments"
    _order = "payment_date desc, name desc"

    register_payment_id = fields.Many2one(store=True,
                                          string=_(u"Register Payments"))
    register_line_ids = fields.One2many('account.register.payments.line',
                                        'payment_id',
                                        string=_(u"Invoices"))

    def set_payment_id_to_lines(self):
        """ Set payment_id in each account_register_payments_line
        """

        ctx = dict(self._context or {})
        register_payments = self.env[
            'account.register.payments'].browse(self.register_payment_id.id)
        register_payments.line_ids.with_context(ctx).write(
            {'payment_id': self.id})

    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment
            references invoice(s) they are reconciled.
            Return the journal entry.
        """

        self.set_payment_id_to_lines()

        if not self.register_payment_id:
            res = super(AccountPayment, self)._create_payment_entry(amount)
            return res

        aml_obj = self.env[
            'account.move.line'].with_context(check_move_validity=False)
        debit, credit, amount_currency = \
            aml_obj.with_context(
                date=self.payment_date).compute_amount_fields(
                    amount, self.currency_id, self.company_id.currency_id)

        move = self.env['account.move'].create(self._get_move_vals())

        # Write line corresponding to invoice payment
        counterpart_aml_dict = self._get_multi_counterpart_move_line_vals(
            move.id)

        for aml_cont in counterpart_aml_dict:
            counterpart_aml = aml_obj.create(aml_cont)
            self.env['account.invoice'].browse(
                aml_cont['invoice_id']).register_payment(counterpart_aml)

        # Write counterpart lines
        liquidity_aml_dict = self._get_shared_move_line_vals(
            credit, debit, -amount_currency, move.id, False)
        liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
        aml_obj.create(liquidity_aml_dict)

        move.post()
        return move

    def _get_multi_counterpart_move_line_vals(self, move_id=False):
        aml_obj = self.env[
            'account.move.line'].with_context(check_move_validity=False)
        move_lines = []
        name = ''
        if self.partner_type == 'customer':
            if self.payment_type == 'inbound':
                name += _(u"Customer Payment")
            elif self.payment_type == 'outbound':
                name += _(u"Customer Refund")
        elif self.partner_type == 'supplier':
            if self.payment_type == 'inbound':
                name += _(u"Vendor Refund")
            elif self.payment_type == 'outbound':
                name += _(u"Vendor Payment")

        for rec in self:
            aprl_ids = self.env[
                'account.register.payments.line'].search(
                    [('register_payment_id', '=',
                      self.register_payment_id.id)])
            for line in aprl_ids:
                name_line = name + ":" + line.invoice_id.number
                credit, debit, amount_currency = \
                    aml_obj.with_context(
                        date=self.payment_date).compute_amount_fields(
                            line.amount,
                            self.currency_id,
                            self.company_id.currency_id)
                move_line = {
                    'partner_id': self.payment_type in
                    ('inbound', 'outbound') and
                    self.env['res.partner']._find_accounting_partner(
                        self.partner_id).id or False,
                    'invoice_id': line.invoice_id and
                    line.invoice_id.id or False,
                    'move_id': move_id,
                    'debit': debit,
                    'credit': credit,
                    'amount_currency': amount_currency or False,
                    'name': name_line,
                    'account_id': self.destination_account_id.id,
                    'journal_id': self.journal_id.id,
                    'currency_id': self.currency_id !=
                    self.company_id.currency_id and
                    self.currency_id.id or False,
                    'payment_id': self.id,
                }
                move_lines.append(move_line)
        return move_lines


class AccountRegisterPayments(models.Model):
    _name = 'account.register.payments'
    _inherit = 'account.register.payments'

    line_ids = fields.One2many('account.register.payments.line',
                               'register_payment_id',
                               string=_(u"Invoices"))

    @api.constrains('amount')
    def _check_total_mustbe_sum_of_lines(self):
        for rec in self:
            if rec.line_ids:
                total_amount_lines = 0.00
                for line in rec.line_ids:
                    total_amount_lines += line.amount
                difference = self.amount - total_amount_lines
                if abs(difference) > 0.05:
                    raise exceptions.ValidationError(_(u"The sum of the amount to \
                                                     pay per invoice '%d'\
                                                     must be equal than \
                                                     the payment amount '%s'")
                                                     % (total_amount_lines,
                                                        self.amount))

    def get_payment_vals(self):
        """ Hook for extension """
        res = super(AccountRegisterPayments, self).get_payment_vals()
        res.update({
            'register_payment_id': self.id,
        })
        return res

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
                'register_payment_id': self.id
            }
            lines.append([0, False, aprl])
        rec.update({
            'line_ids': lines,
        })
        return rec


class AccountRegisterPaymentsLine(models.Model):
    _name = 'account.register.payments.line'
    _description = "stores the invoices payed in this transaction and " \
        + "the amount payed to each one"

    register_payment_id = fields.Many2one(
        'account.register.payments',
        string=_(u"Register payment"),
        required=True,
        ondelete='cascade')
    payment_id = fields.Many2one(
        'account.payment',
        string=_(u"Payment"),
        required=False)
    invoice_id = fields.Many2one(
        'account.invoice',
        string=_(u"Invoice"),
        required=False)
    name = fields.Char(string=_(u"Description"))
    account_id = fields.Many2one(
        'account.account',
        string=_(u"Account"),
        required=True)
    untax_amount = fields.Float(string=_(u"Untax Amount"))
    amount = fields.Float(
        string=_(u"Amount"),
        digits_compute=dp.get_precision('Account'))
    reconcile = fields.Boolean(string=_(u"Full Reconcile"))
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u"Analytic Account"))
    move_line_id = fields.Many2one(
        'account.move.line',
        string=_(u"Journal Item"),
        copy=False)
    date_original = fields.Date(
        related='move_line_id.date',
        string=_(u"Date"),
        readonly=True,
        store=True)
    name = fields.Char(
        string=_(u"Reference/Description"),
        readonly=True)
    origin = fields.Char(
        string=_(u"Source Document"),
        readonly=True)
    reference = fields.Char(
        string=_(u"Vendor Reference"),
        readonly=True)
    partner_id = fields.Many2one(
        related='register_payment_id.partner_id',
        string=_(u"Partner"),
        readonly=True,
        store=True)
    date_due = fields.Date(
        related='move_line_id.date_maturity',
        string=_(u"Due Date"),
        readonly=True,
        store=True)
    company_id = fields.Many2one(
        related='register_payment_id.company_id',
        string=_(u"Company"),
        store=True,
        readonly=True)
    amount_original = fields.Float(
        string=_(u"Original Amount"),
        store=True,
        digits_compute=dp.get_precision('Account'))
    amount_unreconciled = fields.Float(
        string=_(u"Open Balance"),
        store=True,
        digits_compute=dp.get_precision('Account'))
    currency_id = fields.Many2one(
        related='register_payment_id.currency_id',
        string=_(u"Currency"),
        readonly=True,
        store=True)

    @api.onchange('amount')
    def _verify_full_reconcile(self):
        if self.amount == self.amount_unreconciled:
            self.reconcile = True
        else:
            self.reconcile = False

        if self.amount > self.amount_unreconciled:
            return {
                'warning': {
                    'title': _(u"Incorrect 'amount' value"),
                    'message':
                    _(u"The amount to pay for Invoice must be equal or \
                      less than the amount unreconciled"),
                },
            }

        if self.amount < 0:
            return {
                'warning': {
                    'title': _(u"Incorrect 'amount' value"),
                    'message':
                    _(u"The amount to pay for Invoice may not be negative"),
                },
            }

    @api.onchange('reconcile')
    def _verify_full_reconcile2(self):
        if self.reconcile:
            self.amount = self.amount_unreconciled

    _sql_constraints = [
        ('amount_less_than_unreconciled',
         'CHECK(amount <= amount_unreconciled)',
         "The amount to pay for Invoice must be not greater \
                      than the amount unreconciled"),

        ('amount_greater than zero',
         'CHECK(amount >= 0)',
         "The amount to pay for Invoice may not be negative"),
    ]

    @api.constrains('date_original')
    def _check_date_less_than_payment_date(self):
        for rec in self:
            if rec.date_original and rec.date_original >\
                    rec.register_payment_id.payment_date:
                raise exceptions.ValidationError(_(u"The invoices to pay must be not later\
                than the payment"))
