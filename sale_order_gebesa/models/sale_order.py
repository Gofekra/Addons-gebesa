# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.addons import decimal_precision as dp
from openerp.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    notify_approval = fields.Char(
        string=_(u'Notify approval'),
        size=100,
    )

    date_delivery = fields.Date(
        string=_(u'Date delivery'),
        default=fields.Date.today,
    )

    date_reception = fields.Date(
        string=_(u'Date reception'),
        default=fields.Date.today,
    )

    total_net_sale = fields.Float(
        string=_(u'Total net sale'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_freight = fields.Float(
        string=_(u'Freight percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_freight = fields.Float(
        string=_(u'Total Freight'),
        digits_compute=dp.get_precision('Account'),
    )

    perc_installation = fields.Float(
        string=_(u'installation percentage'),
        digits_compute=dp.get_precision('Account'),
    )

    total_installation = fields.Float(
        string=_(u'Total installation'),
        digits_compute=dp.get_precision('Account'),
    )

    profit_margin = fields.Float(
        string=_(u'Profit margin'),
        digits_compute=dp.get_precision('Account'),
    )

    not_be_billed = fields.Boolean(
        string=_(u'not be billed'),
    )

    manufacture = fields.Selection(
        [('special', _(u'Special')),
            ('line', _(u'Line')),
            ('replenishment', _(u'Replenishment')),
            ('semi_special', _(u'Semi special'))],
        string=_(u"Manufacture"),
    )

    executive = fields.Char(
        string=_(u'Executive'),
        size=100,
    )

    respo_reple = fields.Char(
        string=_(u'Responsible of replenishment'),
        size=200,
    )

    priority = fields.Selection(
        [('high', _(u'High')), ('replenishment', _(u'Replenishment')),
         ('express', _(u'Express')), ('sample', _(u'Sample'))],
        _(u'Manufacturing priority'),)

    complement_saleorder_id = fields.Many2one(
        'sale.order',
        string=_(u'In complement:'),
        help=_(u'Displays a list of sales orders'),
    )

    manufacturing_observations = fields.Text(
        string=_(u'Observations Manufacturing'),
    )

    replenishing_motif = fields.Text(
        string=_(u'Reason for the replenishment'),
    )

    credit_status = fields.Selection(
        [('normal', _(u'Normal')),
         ('suspended', _(u'Suspended for Collection')),
         ('conditioned', _(u'Conditioned'))],
        _(u'Credit status'),)

    credit_note = fields.Text(
        string=_(u'Note Credit and Collections'),
    )

    date_production = fields.Date(
        string=_('Date of Production Termination'),
    )

    approve = fields.Selection(
        [('approved', _('Approved')),
         ('suggested', _('Suggested for Approval')),
         ('not_approved', _('Not Approved'))],
        default='not_approved',
        string=_('Approve Status'),
        store=True,
    )

    total_cost = fields.Float(
        string=_('Total cost'),
    )

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The order name must be unique"),
    ]

    @api.multi
    @api.onchange('project_id')
    def onchange_project_id(self):
        """
        Trigger the change of warehouse when the analytic account is modified.
        """
        if self.project_id and self.project_id.warehouse_id:
            self.warehouse_id = self.project_id.warehouse_id
        return {}

    @api.multi
    def action_confirm(self):
        for order in self:
            order.validate_manufacturing()
            if not order.notify_approval:
                raise UserError(
                    _('The following field is not invalid:\nNotify approval'))
            if not order.manufacture:
                raise UserError(
                    _('The following field is not invalid:\nManufacture'))
            if not order.executive:
                raise UserError(
                    _('The following field is not invalid:\nExecutive'))
            if not order.priority:
                raise UserError(
                    _('The following field is not invalid:\nManufacturing \
                      priority'))
            if not order.project_id:
                raise UserError(
                    _('The following field is not invalid:\nAnalytic Account'))
            global_cost = 0.0
            global_net_sale = 0.0
            global_freight = 0.0
            global_installa = 0.0
            global_profit_margin = 0.0
            currency = order.company_id.currency_id
            for line in order.order_line:
                product = line.product_id
                import pdb; pdb.set_trace()
                if product.quotation_product:
                    raise UserError(_('The Product contains Quotation'))
                standard_cost = product.standard_price or 0.0
                # standard_cost = currency.compute(
                #    standard_cost, order.pricelist_id.currency_id) or 0.0
                # if standard_cost > 0:
                # standard_cost = standard_cost
                # * inv.rate
                total_cost = standard_cost * line.product_uom_qty
                perc_freight = order.perc_freight or False
                freight = 0.0
                profit_margin = 0.0
                perc_installation = order.perc_installation or False
                installation = 0.0
                if perc_freight:
                    freight = (line.price_unit * line.product_uom_qty) * (
                        perc_freight / 100.0)
                net_sale = (line.price_unit * line.product_uom_qty) - freight
                if perc_installation:
                    installation = net_sale * (
                        perc_installation / 100.0)
                net_sale = net_sale - installation

                if net_sale > 0.000000:
                    total_pm = currency.compute(
                        total_cost, order.pricelist_id.currency_id)
                    profit_margin = (1 - (total_pm) / net_sale)
                    profit_margin = profit_margin * 100

                line.freight_amount = freight
                line.installation_amount = installation
                line.net_sale = net_sale
                line.profit_margin = profit_margin
                line.purchase_price = standard_cost
                line.standard_cost = total_cost

                global_cost += total_cost
                global_net_sale += net_sale
                global_freight += freight
                global_installa += installation

            if global_net_sale > 0.000000:
                global_total_pm = currency.compute(global_cost, order.pricelist_id.currency_id)
                global_profit_margin = (1 - (global_total_pm) / global_net_sale)
                global_profit_margin = global_profit_margin * 100

            order.total_cost = global_cost
            order.total_net_sale = global_net_sale
            order.total_freight = global_freight
            order.total_installation = global_installa
            order.profit_margin = global_profit_margin

        return super(SaleOrder, self).action_confirm()

    @api.multi
    def validate_manufacturing(self):
        for order in self:

            # pending = self.env['sale.order'].search(
            # [('state', '=', 'draft')])
            dife = 0.0
            dife = order.amount_total - order.total_nste
            if order.total_nste > 0.0000000:
                if abs(dife) > 0.6000:
                    raise UserError(
                        _('The amount are differents:\nAnalytic Account'))

            for line in order.order_line:
                if line.product_id:
                    routes = line.product_id.route_ids + \
                        line.product_id.categ_id.total_route_ids
                    if len(routes) < 2:
                        raise UserError(
                            _('%s %s %s' % (
                                _("The next product has no a valid Route"),
                                line.product_id.default_code,
                                line.product_id.name)))
                    product_bom = False
                    for bom in line.product_id.product_tmpl_id.bom_ids:
                        if bom.product_id.id == line.product_id.id:
                            product_bom = bom or False
                    if not product_bom:
                        raise UserError(
                            _('%s %s %s' % (
                                _("The next product has no a Bill of Materials"),
                                line.product_id.default_code, line.product_id.name)))

        return True

    @api.multi
    def approve_action(self):
        for order in self:
            if order.approve == 'approved':
                raise UserError(_('This Sale Order is already approved'))
        self.write({'approve': 'approved'})
        return True

    @api.multi
    def suggested_action(self):
        for order in self:
            if order.approve == 'suggested':
                raise UserError(_('This Sale Order is already Suggested for Approval'))
        self.write({'approve': 'suggested'})
        return True

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['perc_freight'] = self.perc_freight
        invoice_vals['perc_installation'] = self.perc_installation
        invoice_vals['executive'] = self.executive
        invoice_vals['manufacture'] = self.manufacture

        return invoice_vals

    @api.multi
    def action_done(self):
        super(SaleOrder, self).action_done()
        # commented temporary til implementatio of CRM
        self.force_quotation_send()
