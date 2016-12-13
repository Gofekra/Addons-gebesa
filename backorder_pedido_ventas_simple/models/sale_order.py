# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    week_number = fields.Integer(
        'Numero de la semana',
        compute="_compute_week_number"
    )

    @api.depends('date_order')
    def _compute_week_number(self):
        for sale in self:
         #   campo1 = '02-02-2016 05:00:00',
            campo=str(sale.date_order)
            arreglo= campo.split(" ");
            arreglo2=arreglo[0].split("/");
            cadena_n=("-").join(arreglo2);
            sale.week_number = int(datetime.datetime.strptime(
                cadena_n, '%Y-%m-%d').strftime('%W'))


#datetime.datetime.strptime('28-09-2014', '%d-%m-%Y').strftime('El dia es: %W')