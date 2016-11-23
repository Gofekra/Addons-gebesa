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
        [('low', _(u'Low')), ('medium', _(u'Medium')),
         ('high', _(u'High')), ('replenishment', _(u'Replenishment')),
         ('express', _(u'Express')), ('sample', _(u'Sample')),
         ('complement', _(u'Complement'))],
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

        return super(SaleOrder, self).action_confirm()
