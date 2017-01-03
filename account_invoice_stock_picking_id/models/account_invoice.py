# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    picking_id = fields.Many2one('stock.picking',
                                 ondelete='restrict',
                                 string=_("Related Picking"),
                                 index=True,
                                 readonly=True)

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if not inv.sale_id and not inv.picking_id:
                if not inv.prepayment_ok and inv.type in ['out_invoice']:
                    inv._create_pickings_and_procurements(None)
        return res

    def _create_pickings_and_procurements(self, picking_id=False):
        move_obj = self.env['stock.move']
        picking_obj = self.env['stock.picking']
        procurement_obj = self.env['procurement.order']
        proc_ids = []
        generate = False
        for line in self.invoice_line_ids:
            if line.product_id.type == 'product':
                generate = True

        if generate:
            for line in self.invoice_line_ids:
                date_planned = self._get_date_planned(line)

                if line.product_id:
                    if line.product_id.type in ('product', 'consu'):
                        if not picking_id:
                            picking_id = picking_obj.create(
                                self._prepare_order_picking(line))
                        move_id = move_obj.create(
                            self._prepare_order_line_move(line, picking_id,
                                                          date_planned))
                    else:
                        move_id = False

                    proc_id = procurement_obj.create(
                        self._prepare_order_line_procurement(
                            line, move_id, date_planned))
                    proc_ids.append(proc_id)
                    line.procurement_id = proc_id
                    self.ship_recreate(line, move_id, proc_id)

        if picking_id:
            for picking in picking_id:
                picking.action_confirm()
                for move in picking.move_lines:
                    move.force_assign()
                picking.do_transfer()

        for proc_id in proc_ids:
            proc_id.run()

        if picking_id:
            self.picking_id = picking_id
        return True

    def _get_date_planned(self, line):
        start_date = self.date_to_datetime(self.date_invoice)
        date_planned = datetime.strptime(
            start_date, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(
            days=0.0)
        date_planned = (date_planned - timedelta(
                        days=self.company_id.security_lead)
                        ).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return date_planned

    def _prepare_order_picking(self, line):
        picking_name = self.env['ir.sequence'].get('stock.picking')
        warehouse_id = self.account_analytic_id.warehouse_id
        move_type_obj = self.env['stock.move.type']
        move_type_id = move_type_obj.search([('code', '=', 'S1')]) or False
        return {
            'name': picking_name,
            'origin': self.name,
            'date': self.date_to_datetime(self.date_invoice),
            'type': 'out',
            'state': 'waiting',
            'move_type': 'direct',
            'invoice_id': self.id,
            'partner_id': self.partner_shipping_id.id,
            'note': self.comment,
            'account_analytic_id': self.account_analytic_id.id,
            'invoice_state': 'invoiced',
            'company_id': self.company_id.id,
            'stock_move_type_id': move_type_id[0].id,
            'location_id': warehouse_id.wh_output_stock_loc_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'picking_type_id': warehouse_id.out_type_id.id
        }

    def date_to_datetime(self, userdate):
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATE_FORMAT)
        if self._context and self._context.get('tz'):
            tz_name = self._context['tz']
        else:
            tz_name = self.env['res.users'].browse(self._uid).read(
                ['tz'])[0]['tz']
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            user_datetime = user_date + relativedelta(hours=12.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _prepare_order_line_procurement(self, line, move_id, date_planned):
        warehouse_id = self.account_analytic_id.warehouse_id
        return{
            'name': line.name[:50],
            'origin': self.name,
            'date_planned': date_planned,
            'product_id': line.product_id.id,
            'product_qty': line.quantity,
            'product_uom': line.product_id.uom_id.id,
            'product_uos_qty': line.product_id.uom_id.id,
            'product_uos': line.product_id.uom_id.id,
            'location_id': warehouse_id.wh_output_stock_loc_id.id,
            'move_id': move_id,
            'company_id': self.company_id.id,
            'note': line.name,
        }

    def ship_recreate(self, line, move_id, proc_id):
        move_obj = self.env['stock.move']
        proc_obj = self.env['procurement.order']

        if move_id and self.state == 'shipping_except':
            cur_mov = move_obj.browse(move_id)
            moves = []
            for pick in self.picking_ids:
                if pick.id != cur_mov.picking_id.id and pick.state != 'cancel':
                    moves.extend(
                        move for move in pick.move_lines if move.state !=
                        'cancel' and move.invoice_line_id.id == line.id)
            if moves:
                product_qty = cur_mov.product_qty
                product_uos_qty = cur_mov.product_uos_qty
                for move in moves:
                    product_qty -= move.product_qty
                    product_uos_qty -= move.product_uos_qty
                if product_qty > 0 or product_uos_qty > 0:
                    move_id.product_qty = product_qty
                    move_id.product_uos_qty = product_uos_qty
                    proc_id.product_qty = product_qty
                    proc_id.product_uos_qty = product_uos_qty
                else:
                    cur_mov.unlink()
                    proc_obj.unlink([proc_id])
        return True

    def _prepare_order_line_move(self, line, picking_id, date_planned):
        warehouse_id = self.account_analytic_id.warehouse_id
        location_id = warehouse_id.wh_output_stock_loc_id.id
        output_id = self.partner_id.property_stock_customer.id
        move_type_obj = self.env['stock.move.type']
        move_type_id = move_type_obj.search([('code', '=', 'S1')]) or False
        return{
            'name': line.name[:50],
            'picking_id': picking_id.id,
            'product_id': line.product_id.id,
            'date': date_planned,
            'date_expected': date_planned,
            'product_uom_qty': line.quantity,
            'product_uom': line.product_id.uom_id.id,
            'product_uos_qty': line.product_id.uom_id.id,
            'product_uos': line.product_id.uom_id.id,
            'product_packaging': False,
            'partner_id': self.partner_shipping_id.id,
            'location_id': location_id,
            'location_dest_id': output_id,
            'invoice_line_id': line.id,
            'tracking_id': False,
            'company_id': self.company_id.id,
            'price_unit': line.product_id.standard_price or 0.0,
            'stock_move_type_id': move_type_id[0].id,
        }
