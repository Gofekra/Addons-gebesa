# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from openerp import _, api, fields, models
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import ValidationError


class stock_quant(osv.osv):
    _inherit = 'stock.quant'

    def _get_accounting_data_for_valuation(self, cr, uid, move, context=None):
        """
        Return the accounts and journal to use to post Journal Entries for
        the real-time
        valuation of the quant.

        :param context: context dictionary that can explicitly mention the
        company to consider via the 'force_company' key
        :returns: journal_id, source account, destination account, valuation
        account
        :raise: openerp.exceptions.UserError if any mandatory account or
        journal is not defined.
        """
        product_obj = self.pool.get('product.template')
        accounts = product_obj.browse(
            cr, uid, move.product_id.product_tmpl_id.id,
            context).get_product_accounts()

        if move.location_id.valuation_out_account_id:
            acc_src = move.location_id.valuation_out_account_id.id
        else:
            acc_src = accounts['stock_input'].id

        if move.location_dest_id.valuation_in_account_id:
            acc_dest = move.location_dest_id.valuation_in_account_id.id
        else:
            acc_dest = accounts['stock_output'].id

        # Cesar Barron 09 Ago 2016 ##########
        # acc_valuation = accounts.get('stock_valuation', False)
        pick_type = move.picking_id.picking_type_id.code or False

        if pick_type:
            if pick_type == 'incoming':
                acc_valuation = move.location_dest_id.account_id or False
            elif pick_type == 'outgoing':
                acc_valuation = move.location_id.account_id or False
                acc_dest = move.location_dest_id.account_id.id or False
                if move.location_id.usage not in ('internal', 'transit', 'customer') and move.location_dest_id.usage == 'internal':
                    acc_src = acc_valuation.id
                    acc_valuation = move.location_dest_id.account_id
            elif pick_type == 'internal':
                acc_valuation = move.location_id.account_id or False
            else:
                acc_valuation = move.location_id.account_id or False
        else:
            acc_valuation = move.location_id.account_id or False

        if not acc_valuation:
            acc_valuation = accounts.get('stock_valuation', False)
        # Cesar Barron 09 Ago 2016 ##########

        if acc_valuation:
            acc_valuation = acc_valuation.id
        if not accounts.get('stock_journal', False):
            raise ValidationError(
                _('You don\'t have any stock journal defined on '
                  'your product category, check if you have installed '
                  'a chart of accounts'))
        if not acc_src:
            raise ValidationError(
                _('Cannot find a stock input account for the '
                  'product %s. You must define one on the product '
                  'category, or on the location, before processing this '
                  'operation.') % (move.product_id.name))
        if not acc_dest:
            raise ValidationError(
                _('Cannot find a stock output account for the '
                  'product %s. You must define one on the product category, '
                  'or on the location, before processing this '
                  'operation.') % (move.product_id.name))
        if not acc_valuation:
            raise ValidationError(
                _('You don\'t have any stock valuation account defined on '
                  'your product category. You must define one before '
                  'processing this operation.'))
        journal_id = accounts['stock_journal'].id
        return journal_id, acc_src, acc_dest, acc_valuation

    def _prepare_account_move_line(self, cr, uid, move, qty, cost,
                                   credit_account_id, debit_account_id,
                                   context=None):
        """
        Generate the account.move.line values to post to track
        the stock valuation difference due to the
        processing of the given quant.
        """
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        if context.get('force_valuation_amount'):
            valuation_amount = context.get('force_valuation_amount')
        else:
            if move.product_id.cost_method == 'average':
                valuation_amount =\
                    cost if move.location_id.usage != 'internal' and\
                    move.location_dest_id.usage == 'internal' else\
                    move.product_id.standard_price
            else:
                valuation_amount =\
                    cost if move.product_id.cost_method ==\
                    'real' else move.product_id.standard_price
        # the standard_price of the product may be in another decimal
        # precision, or not compatible with the coinage of
        # the company currency... so we need to use round()
        # before creating the accounting entries.
        valuation_amount = currency_obj.round(
            cr, uid, move.company_id.currency_id, valuation_amount * qty)
        # check that all data is correct
        if move.company_id.currency_id.is_zero(valuation_amount):
            raise ValidationError(
                _("The found valuation amount for product %s is zero. "
                  "Which means there is probably a configuration error. "
                  "Check the costing method and the "
                  "standard price") % (move.product_id.name,))

        partner_id = (
            move.picking_id.partner_id and self.pool.get(
                'res.partner')._find_accounting_partner(
                    move.picking_id.partner_id).id) or False

        # Cesar Barron 09 Ago 2016 ####
        reference = False
        name = False
        # trace = move.location_id.name + "->" + move.location_dest_id.name
        if move.picking_id and not move.production_id and not move.raw_material_production_id:
            reference = move.picking_id.name
            # + " " + trace or False
            name = move.picking_id.name + " " + move.name
        elif move.production_id:
            reference = move.production_id.name
            # + " " + trace or False
            name = move.name + ' [' + move.product_id.default_code + '] ' + move.product_id.name
        elif move.raw_material_production_id:
            reference = move.raw_material_production_id.name
            # + " " + trace or False
            name = move.name + ' [' + move.product_id.default_code + '] ' + move.product_id.name
        else:
            reference = "W/O Reference "
            name = move.product_id.name
            # + trace

        analytic_id = move.location_id.account_analytic_id.id or False
        # Cesar Barron 09 Ago 2016 ####

        debit_line_vals = {
            'name': name,
            'product_id': move.product_id.id,
            'quantity': qty,
            'product_uom_id': move.product_id.uom_id.id,
            # 'ref': move.picking_id and move.picking_id.name or False,
            'ref': reference,
            'analytic_account_id': analytic_id,
            'partner_id': partner_id,
            'debit': valuation_amount > 0 and valuation_amount or 0,
            'credit': valuation_amount < 0 and -valuation_amount or 0,
            'account_id': debit_account_id,
        }
        credit_line_vals = {
            'name': name,
            'product_id': move.product_id.id,
            'quantity': qty,
            'product_uom_id': move.product_id.uom_id.id,
            # 'ref': move.picking_id and move.picking_id.name or False,
            'ref': reference,
            'analytic_account_id': analytic_id,
            'partner_id': partner_id,
            'credit': valuation_amount > 0 and valuation_amount or 0,
            'debit': valuation_amount < 0 and -valuation_amount or 0,
            'account_id': credit_account_id,
        }
        return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]

    def _create_account_move_line(self, cr, uid, quants, move,
                                  credit_account_id, debit_account_id,
                                  journal_id, context=None):
        # group quants by cost
        quant_cost_qty = {}
        for quant in quants:
            if quant_cost_qty.get(quant.cost):
                quant_cost_qty[quant.cost] += quant.qty
            else:
                quant_cost_qty[quant.cost] = quant.qty
        move_obj = self.pool.get('account.move')

        # picking_obj = self.pool.get('stock.picking')
        for cost, qty in quant_cost_qty.items():

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

            move_lines = self._prepare_account_move_line(
                cr, uid, move, qty, cost, credit_account_id,
                debit_account_id, context=context)
            date = context.get('force_period_date',
                               # fields.Date.context_today(self)
                               fields.date.context_today(
                                   self, cr, uid, context=context)
                               )
            new_move = move_obj.create(
                cr, uid, {'journal_id': journal_id,
                          'line_ids': move_lines,
                          'date': date,
                          # 'ref': move.picking_id.name
                          'ref': reference
                          }, context=context)
            move_obj.post(cr, uid, [new_move], context=context)
            move.acc_move_id = new_move
            # if move.picking_id:
            #     picking_obj.write(
            #         cr, uid, [move.picking_id.id], {'am_ids': [4, new_move]},
            #         context=context)
            # move_ids.append(new_move)
