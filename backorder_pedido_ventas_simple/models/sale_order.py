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
        compute="_compute_week_number",
        store=True,  # STORE DEL NUMERO DE SEMANA
    )

    coint = fields.Char(
        'Moneda',
        compute="_compute_coin"
    )

    rate_mex = fields.Float(
        'Rate',
        compute="_compute_rate_mex",
        digits_compute=dp.get_precision('Account')
    )

    total_rate_mex = fields.Float(
        'Total MXN',
        compute="_compute_total_rate_",)

    freight_rate_mex = fields.Float(
        'Flete MXN',
        compute="_compute_total_rate_",
    )

    installation_rate_mex = fields.Float(
        'Instalación MXN',
        compute="_compute_total_rate_",
    )
    net_sale_rate_mex = fields.Float(
        'Vta Neta MXN',
        compute="_compute_total_rate_",
        store=True,  #CAMPO DEL NET SALE MEX
    )

    amount_pending_mex = fields.Float(
        'Imp X Sur MXN',
        compute="_compute_total_rate_",
    )

    @api.depends('pricelist_id.currency_id')
    def _compute_coin(self):
        # currency_obj = self.env['res.currency']
        for sale in self:
            currency_id = sale.pricelist_id.currency_id.name
            sale.coint = currency_id

    @api.depends('pricelist_id.currency_id', 'date_order')
    def _compute_rate_mex(self):
        # pricelist_obj = self.env['product.pricelist']
        # date = context.get('date_order')
        # currency_id = contex.get('pricelist_id.currency_id')
        # company_id = context.get('company_id')
        for sale in self:
            date = sale.date_order
            currency_id = sale.pricelist_id.currency_id.id
            company_id = sale.company_id.id
            self._cr.execute("""SELECT rate_mex From res_currency_rate
                            WHERE currency_id = %s
                            AND CAST(name AS DATE) = CAST(%s AS DATE)
                            AND (company_id is null
                                OR company_id = %s)
                            """, (currency_id, date, company_id))
            if self._cr.rowcount:
                sale.rate_mex = self._cr.fetchone()[0]
            else:
                sale.rate_mex = 1
        return sale.rate_mex

    @api.depends('amount_total', 'rate_mex')
    def _compute_total_rate_(self):
        for sale in self:
            amount = sale.amount_untaxed
            freight = sale.total_freight
            installation = sale.total_installation
            net_sale = sale.total_net_sale
            rate = sale.rate_mex
            pending = sale.amount_pending
            sale.total_rate_mex = amount * rate
            sale.freight_rate_mex = freight * rate
            sale.installation_rate_mex = installation * rate
            sale.net_sale_rate_mex = net_sale * rate
            sale.amount_pending_mex = pending * rate

    @api.depends('date_order')
    def _compute_week_number(self):
        for sale in self:
         #   campo1 = '02/02/2016 05:00:00',
            campo=str(sale.date_order)
            #en este paso la cadena campo se cortan los espacios
            #por lo que se crea un arreglo de dos cadenas
            #quedando asi-->campo= '02/02/201605:00:00'            
            arreglo= campo.split(" ");
            #se toma como referencia la cadena de la primera posicion
            #es este paso se cortan los / de la cadena.
            #quedando asi -->arreglo2='02022016' 
            arreglo2=arreglo[0].split("/");
            #ahora solo se unen por medio de guiones y se guarda en una cadena alterna 
            cadena_n=("-").join(arreglo2);

            sale.week_number = int(datetime.datetime.strptime(
                cadena_n, '%Y-%m-%d').strftime('%W'))


#datetime.datetime.strptime('28-09-2014', '%d-%m-%Y').strftime('El dia es: %W')