# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
import time


class IntegrationCostGebesa(models.Model):
    _name = 'integration.cost.gebesa'
    _description = 'Integration cost gebesa'

    def _get_journal(self):
        journal_obj = self.env['account.journal']
        user = self.env['res.users'].browse(self._uid)
        company_id = self._context.get('company_id', user.company_id.id)
        domain = [('company_id', '=', company_id)]
        domain.append(('integration_cost', '=', True))
        res = journal_obj.search(domain)
        return res and res[0] or False

    name = fields.Char(
        string=_(u'Name'),
        size=256,
        help=_(u'Description of this integration costs'),
    )
    date = fields.Date(
        string=_(u'Date'),
        default=fields.Date.today,
    )
    date_post = fields.Date(
        string=_(u'Accounting date'),
        help=_(u'Date used for the accounting entry'),
        default=fields.Date.today,
    )
    state = fields.Selection(
        [('draf', _(u'Draf')),
         ('cancel', _(u'Cancel')),
         ('done', _(u'Done'))],
        string=_(u"State"),
        default='draf'
    )
    company_id = fields.Many2one(
        'res.company',
        string=_(u'Company'),
        default=lambda self: self.env['res.users'].browse(
            self._uid).company_id.id
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Partner'),
        help=_(u'Supplier of raw material')
    )
    journal_id = fields.Many2one(
        'account.journal',
        string=_(u'Journal'),
        help=_(u'Accounting journal where entries will be posted'),
        default=_get_journal
    )
    move_id = fields.Many2one(
        'account.move',
        string=_(u'Accounting entry'),
    )
    invoice_mp_ids = fields.Many2many(
        'account.invoice',
        'gic_invoice_mat',
        'gic_id',
        'inv_id',
        string=_(u'Invoices raw material'),
    )
    invoice_adi_ids = fields.Many2many(
        'account.invoice',
        'gic_invoice_adi',
        'gic_id',
        'inv_id',
        string=_(u'Additional invoices'),
    )
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string=_(u'Analytic account'),
        states={'draft': [('readonly', False)]}
    )
    disc_additional = fields.Selection(
        [('value', _(u'Value')),
         ('quantity', _(u'Quantity'))],
        string=_(u"Type apportionment"),
        help=_(u'It defines how the additional costs are apportioned \
               between the lines of the invoice'),
        default='value',
    )

    def validate_data(self):
        ids = [res.id for res in self]
        gic = self.browse(ids[0])
        res = []
        res.append(gic.invoice_mp_ids and True or False)
        res.append(gic.invoice_adi_ids and True or False)

        if all(res):
            return True
        else:
            raise ValidationError(_(u"Integration should have as much raw \
                                  material invoices as additional invoices"))

    @api.multi
    def integrates_costs(self):
        aml_obj = self.env['account.move.line']
        am_obj = self.env['account.move']

        ids = [res.id for res in self]
        self.validate_data()

        res = {}
        ctx = self._context.copy()
        name = time.strftime('%Y-%m-%d')
        ctx.update({'date': name})

        int_cost = self.browse(ids[0])

        for inv in int_cost.invoice_adi_ids:
            inv.integration_id = int_cost.id
        for inv in int_cost.invoice_mp_ids:
            inv.integration_id = int_cost.id

        date = int_cost.date_post or fields.Date.today
        ref = int_cost.name or ''
        company_id = int_cost.company_id.id
        if not company_id:
            company_id = self.env['res.users'].browse(
                self._uid).company_id.id

        am_vals = {
            'journal_id': int_cost.journal_id.id,
            'date': date,
            'ref': ref,
            'company_id': company_id,
        }

        am_id = am_obj.create(am_vals)

        concat = []

        for inv in int_cost.invoice_adi_ids:
            for line_inv in inv.invoice_line_ids:
                total_quantity = 0.0
                total_price = 0.0
                for inv2 in int_cost.invoice_mp_ids:
                    for line_inv2 in inv2.invoice_line_ids:
                        total_quantity += line_inv2.quantity
                        total_price += line_inv2.price_unit

                for inv2 in int_cost.invoice_mp_ids:
                    for line_inv2 in inv2.invoice_line_ids:
                        account_expense = line_inv.product_id.categ_id.\
                            property_account_expense_categ_id.id or False
                        account_price_difference = line_inv2.product_id.\
                            property_account_creditor_price_difference.id \
                            or False

                        if not account_expense:
                            raise ValidationError(
                                _(u"It is not set up an Expense Account in \
                                  the category of the %s product" %
                                  line_inv.product_id.name_template))
                        if not account_price_difference:
                            raise ValidationError(
                                _(u"It is not set up an price difference Account in \
                                    the product %s" %
                                    line_inv2.product_id.name_template))

                        amount_line = line_inv2.quantity or 0.0
                        price_line = line_inv2.price_unit or 0.0
                        if int_cost.disc_additional == 'quantity':
                            factor = (amount_line * 100.0) / total_quantity
                            factor = factor / 100.0
                        else:
                            factor = (price_line * 100.0) / total_price
                            factor = factor / 100.0

                        ctx = self._context.copy()
                        ctx.update({'date': inv.date_invoice})

                        exchange_rate_dict = inv.currency_id.with_context(
                            ctx)._get_current_rate(name, None)
                        rate = exchange_rate_dict[inv.currency_id.id]

                        amount = line_inv.price_subtotal * factor / rate

                        ctx.update({'check_move_validity': False})
                        vals = {
                            'move_id': am_id.id,
                            'partner_id': inv.partner_id.id,
                            'journal_id': inv2.journal_id.id,
                            'date': int_cost.date_post,
                            'product_id': line_inv2.product_id.id,
                            'credit': amount,
                            'name': line_inv.product_id.name + ' ' +
                            line_inv2.product_id.name,
                            'account_id': account_expense,
                            'analytic_account_id': int_cost.
                            account_analytic_id.id,
                            'debit': 0.0,
                        }
                        aml_obj.with_context(ctx).create(vals)

                        vals = {
                            'move_id': am_id.id,
                            'partner_id': inv.partner_id.id,
                            'journal_id': inv2.journal_id.id,
                            'date': int_cost.date_post,
                            'product_id': line_inv2.product_id.id,
                            'credit': 0.0,
                            'name': line_inv.product_id.name + ' ' +
                            line_inv2.product_id.name,
                            'account_id': account_price_difference,
                            'analytic_account_id': int_cost.
                            account_analytic_id.id,
                            'debit': amount,
                        }
                        aml_obj.with_context(ctx).create(vals)

                        concat_vals = (
                            inv2.picking_id,
                            line_inv.product_id.name,
                            line_inv2.product_id.name,
                            amount,
                            line_inv2.product_id.default_code,
                            line_inv.product_id.name
                        )
                        concat.append(concat_vals)

        am_id.post()

        self[0].move_id = am_id
        self[0].state = 'done'
        return concat
