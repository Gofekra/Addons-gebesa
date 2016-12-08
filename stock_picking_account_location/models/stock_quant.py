# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from openerp.exceptions import ValidationError, UserError
from collections import defaultdict


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def _get_accounting_data_for_valuation(self):
        """ Return the accounts and journal to use to post Journal Entries for
        the real-time valuation of the quant. """
        self.ensure_one()
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()

        if self.location_id.valuation_out_account_id:
            acc_src = self.location_id.valuation_out_account_id.id
        else:
            acc_src = accounts_data['stock_input'].id

        if self.location_dest_id.valuation_in_account_id:
            acc_dest = self.location_dest_id.valuation_in_account_id.id
        else:
            acc_dest = accounts_data['stock_output'].id

        # Cesar Barron 09 Ago 2016 ##########
        # acc_valuation = accounts.get('stock_valuation', False)
        pick_type = self.picking_id.picking_type_id.code or False

        if pick_type:
            if pick_type == 'incoming':
                acc_valuation = self.location_dest_id.account_id or False
            elif pick_type == 'outgoing':
                acc_valuation = self.location_id.account_id or False
                acc_dest = self.location_dest_id.account_id.id or False
                if self.location_id.usage not in (
                    'internal', 'transit', 'customer') and\
                        self.location_dest_id.usage == 'internal':
                    acc_src = acc_valuation.id
                    acc_valuation = self.location_dest_id.account_id
            elif pick_type == 'internal':
                acc_valuation = self.location_id.account_id or False
            else:
                acc_valuation = self.location_id.account_id or False
        else:
            acc_valuation = self.location_id.account_id or False

        if not acc_valuation:
            acc_valuation = accounts_data.get('stock_valuation', False)
        # Cesar Barron 09 Ago 2016 ##########

        acc_valuation = accounts_data.get('stock_valuation', False)
        if acc_valuation:
            acc_valuation = acc_valuation.id
        if not accounts_data.get('stock_journal', False):
            raise UserError(_('You don\'t have any stock journal defined on \
                            your product category, check if you have \
                            installed a chart of accounts'))
        if not acc_src:
            raise UserError(_('Cannot find a stock input account for the \
                            product %s. You must define one on the product \
                            category, or on the location, before processing \
                            this operation.') % (self.product_id.name))
        if not acc_dest:
            raise UserError(_('Cannot find a stock output account for the \
                            product %s. You must define one on the product \
                            category, or on the location, before processing \
                            this operation.') % (self.product_id.name))
        if not acc_valuation:
            raise UserError(_('You don\'t have any stock valuation account \
                            defined on your product category. You must define \
                            one before processing this operation.'))
        journal_id = accounts_data['stock_journal'].id
        return journal_id, acc_src, acc_dest, acc_valuation

    def _prepare_account_move_line(self, qty, cost, credit_account_id,
                                   debit_account_id):
        """
        Generate the account.move.line values to post to track the stock
        valuation difference due to the processing of the given quant.
        """
        self.ensure_one()

        if self._context.get('force_valuation_amount'):
            valuation_amount = self._context.get('force_valuation_amount')
        else:
            if self.product_id.cost_method == 'average':
                valuation_amount =\
                    cost if self.location_id.usage == 'supplier' and\
                    self.location_dest_id.usage == 'internal' else\
                    self.product_id.standard_price
            else:
                valuation_amount = cost if self.product_id.cost_method ==\
                    'real' else self.product_id.standard_price
        # the standard_price of the product may be in another decimal
        # precision, or not compatible with the coinage of the company
        # currency... so we need to use round() before creating the
        # accounting entries.

        debit_value = self.company_id.currency_id.round(valuation_amount * qty)

        # check that all data is correct
        if self.company_id.currency_id.is_zero(debit_value):
            if self.product_id.cost_method == 'standard':
                raise UserError(_("The found valuation amount for product %s \
                                is zero. Which means there is probably a \
                                configuration error. Check the costing method \
                                and the standard price") % (
                    self.product_id.name,))
            return []
        credit_value = debit_value

        if self.product_id.cost_method == 'average' and\
                self.company_id.anglo_saxon_accounting:
            # in case of a supplier return in anglo saxon mode, for products
            # in average costing method, the stock_input account books the real
            # purchase price, while the stock account books the average price.
            # The difference is booked in the dedicated price difference
            # account.
            if self.location_dest_id.usage == 'supplier' and\
                    self.origin_returned_move_id and\
                    self.origin_returned_move_id.purchase_line_id:
                debit_value = self.origin_returned_move_id.price_unit * qty
            # in case of a customer return in anglo saxon mode, for products in
            # average costing method, the stock valuation is made using the
            # original average price to negate the delivery effect.
            if self.location_id.usage == 'customer' and\
                    self.origin_returned_move_id:
                debit_value = self.origin_returned_move_id.price_unit * qty
                credit_value = debit_value
        partner_id = (self.picking_id.partner_id and self.env[
                      'res.partner']._find_accounting_partner(
            self.picking_id.partner_id).id) or False

        # Cesar Barron 09 Ago 2016 ####
        reference = False
        name = False
        if self.picking_id and not self.production_id and\
                not self.raw_material_production_id:
            reference = self.picking_id.name
            # + " " + trace or False
            name = self.picking_id.name + " " + self.name
        elif self.production_id:
            reference = self.production_id.name
            name = self.name + \
                ' [' + self.product_id.default_code + '] ' + \
                self.product_id.name
        elif self.raw_material_production_id:
            reference = self.raw_material_production_id.name
            # + " " + trace or False
            name = self.name + \
                ' [' + self.product_id.default_code + '] ' + \
                self.product_id.name
        else:
            reference = "W/O Reference "
            name = self.product_id.name

        analytic_id = self.location_id.account_analytic_id.id or False
        # Cesar Barron 09 Ago 2016 ####

        debit_line_vals = {
            # 'name': self.name,
            'name': name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            # 'ref': self.picking_id.name,
            'ref': reference,
            'analytic_account_id': analytic_id,
            'partner_id': partner_id,
            'debit': debit_value,
            'credit': 0,
            'account_id': debit_account_id,
        }
        credit_line_vals = {
            # 'name': self.name,
            'name': name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            # 'ref': self.picking_id.name,
            'ref': reference,
            'analytic_account_id': analytic_id,
            'partner_id': partner_id,
            'credit': credit_value,
            'debit': 0,
            'account_id': credit_account_id,
        }
        res = [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
        if credit_value != debit_value:
            # for supplier returns of product in average costing method, in
            # anglo saxon mode
            diff_amount = debit_value - credit_value
            price_diff_account =\
                self.product_id.property_account_creditor_price_difference
            if not price_diff_account:
                price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
            if not price_diff_account:
                raise UserError(
                    _('Configuration error. Please configure the price \
                      difference account on the product or its category to \
                      process this operation.'))
            price_diff_line = {
                # 'name': self.name,
                'name': name,
                'product_id': self.product_id.id,
                'quantity': qty,
                'product_uom_id': self.product_id.uom_id.id,
                # 'ref': self.picking_id.name,
                'ref': reference,
                'analytic_account_id': analytic_id,
                'partner_id': partner_id,
                'credit': diff_amount > 0 and diff_amount or 0,
                'debit': diff_amount < 0 and -diff_amount or 0,
                'account_id': price_diff_account.id,
            }
            res.append((0, 0, price_diff_line))
        return res

    def _create_account_move_line(self, move, credit_account_id,
                                  debit_account_id, journal_id):
        # group quants by cost
        quant_cost_qty = defaultdict(lambda: 0.0)
        for quant in self:
            quant_cost_qty[quant.cost] += quant.qty

        move_obj = self.env['account.move']
        for cost, qty in quant_cost_qty.iteritems():

            # Cesar Barron 09 Ago 2016 ####
            reference = False
            if move.picking_id:
                reference = move.picking_id.name or False
            elif move.production_id:
                reference = move.production_id.name or False
            elif move.raw_material_production_id:
                reference = move.raw_material_production_id.name or False
            else:
                reference = "W/O Reference"
            # Cesar Barron 09 Ago 2016 ####

            move_lines = move._prepare_account_move_line(
                qty, cost, credit_account_id, debit_account_id)
            if move_lines:
                date = self._context.get(
                    'force_period_date', fields.Date.context_today(self))
                new_account_move = move_obj.create({
                    'journal_id': journal_id,
                    'line_ids': move_lines,
                    'date': date,
                    # 'ref': move.picking_id.name
                    'ref': reference})
                new_account_move.post()
                move.acc_move_id = new_account_move
