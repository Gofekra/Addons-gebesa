# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_justification = fields.Char(
        string=_(u'P. M. justification'),
        size=100,
        help=_(u'low-margin justification for the sales order'),
    )

    net_sale = fields.Float(
        string=_(u'Net sales'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    freight_amount = fields.Float(
        string=_(u'Freight amount'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    installation_amount = fields.Float(
        string=_(u'installation amount'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    standard_cost = fields.Float(
        string=_(u'Standard cost'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    profit_margin = fields.Float(
        string=_(u'Profit margin'),
        digits_compute=dp.get_precision('Account'),
        compute='_compute_profit_margin',
        store=True
    )

    low_mu = fields.Boolean(
        string=_(u'Bajo M.U.'),
        compute='_compute_low_mu',
        default=False
    )

    volume = fields.Float(
        string=_('Volume'),
        related='product_id.volume'
    )
    #  @api.multi
    # def _check_mu(self):
    #    for record in self:
    #       record.product_id.product_templ_id.group_id.mu.min
    #      if mugroup > 0:
    #         if mugroup > record.profit_margin
    #            record.low_mu = True
    #   else:
    #      muline = record.product_id.product_templ_id.line_id.mu.min
    #      if muline > 0:

    @api.depends('profit_margin', 'price_unit', 'order_id.perc_freight',
                 'order_id.perc_installation')
    def _compute_low_mu(self):
        for record in self:
            mugroup = record.product_id.product_tmpl_id.group_id.mu_min
            muline = record.product_id.product_tmpl_id.line_id.mu_min
            if mugroup > 0:
                if mugroup > record.profit_margin:
                    record.low_mu = True
            elif muline > 0:
                if muline > record.profit_margin:
                    record.low_mu = True

    @api.depends('price_unit', 'product_uom_qty', 'order_id.perc_freight',
                 'order_id.perc_installation')
    def _compute_profit_margin(self):
        for record in self:
            currency = record.order_id.company_id.currency_id
            product = record.product_id
            standard_cost = product.standard_price or 0.0
            total_cost = standard_cost * record.product_uom_qty
            perc_freight = record.order_id.perc_freight or False
            freight = 0.0
            profit_margin = 0.0
            perc_installation = record.order_id.perc_installation or False
            installation = 0.0
            if perc_freight:
                freight = (record.price_unit * record.product_uom_qty) * (
                    perc_freight / 100.0)
            net_sale = (record.price_unit * record.product_uom_qty) - freight
            if perc_installation:
                installation = net_sale * (
                    perc_installation / 100.0)
            net_sale = net_sale - installation

            if net_sale > 0.000000:
                total_pm = currency.compute(
                    total_cost, record.order_id.pricelist_id.currency_id)
                profit_margin = (1 - (total_pm) / net_sale)
                profit_margin = profit_margin * 100

            record.freight_amount = freight
            record.installation_amount = installation
            record.net_sale = net_sale
            record.profit_margin = profit_margin
            record.purchase_price = standard_cost
            record.standard_cost = total_cost
