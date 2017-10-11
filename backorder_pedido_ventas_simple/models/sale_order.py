# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
import datetime
from openerp.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    week_number = fields.Integer(
        'Numero de la semana',
    )
    # currency_id = fields.Many2one(
    #     'res.currency',
    #     string='Moneda',
    # )
    rate_mex = fields.Float(
        'Rate',
        digits_compute=dp.get_precision('Account')
    )
    total_rate_mex = fields.Float(
        'Total MXN',
    )
    freight_rate_mex = fields.Float(
        'Flete MXN',
    )
    installation_rate_mex = fields.Float(
        'Instalación MXN',
    )
    net_sale_rate_mex = fields.Float(
        'Vta Neta MXN',
    )
    amount_pending_mex = fields.Float(
        'Imp X Sur MXN',
        compute="compute_amount_pending_mex",
    )

    @api.depends('amount_pending', 'rate_mex')
    def compute_amount_pending_mex(self):
        for sale in self:
            pending = sale.amount_pending
            sale.amount_pending_mex = pending * sale.rate_mex

    @api.multi
    def extra_data(self):
        for sale in self:
            # sale.currency_id = sale.pricelist_id.currency_id.id
            self._cr.execute("""SELECT rate_mex From res_currency_rate
                            WHERE currency_id = %s
                            AND CAST(name AS DATE) = CAST(%s AS DATE)
                            AND (company_id is null
                                OR company_id = %s)
                            """, (sale.currency_id.id,
                                  sale.date_order, sale.company_id.id))
            if self._cr.rowcount:
                sale.rate_mex = self._cr.fetchone()[0]
            else:
                sale.rate_mex = 1

            sale.total_rate_mex = sale.rate_mex * sale.amount_untaxed
            sale.freight_rate_mex = sale.rate_mex * sale.total_freight
            sale.installation_rate_mex = sale.rate_mex * sale.total_installation
            sale.net_sale_rate_mex = sale.rate_mex * sale.total_net_sale

    @api.multi
    def action_done(self):
        super(SaleOrder, self).action_done()
        self.extra_data()

    @api.model
    def create(self, vals):
        if 'date_order' in vals.keys():
            campo = str(vals['date_order'])
            arreglo = campo.split(" ")
            arreglo2 = arreglo[0].split("/")
            cadena_n = ("-").join(arreglo2)
            week_number = int(datetime.datetime.strptime(
                cadena_n, '%Y-%m-%d').strftime('%W'))
            vals['week_number'] = week_number
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, values):
        if 'date_order' in values.keys():
            campo = str(values['date_order'])
            arreglo = campo.split(" ")
            arreglo2 = arreglo[0].split("/")
            cadena_n = ("-").join(arreglo2)
            week_number = int(datetime.datetime.strptime(
                cadena_n, '%Y-%m-%d').strftime('%W'))
            values['week_number'] = week_number
        return super(SaleOrder, self).write(values)
