# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def _get_current_rate(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        res = {}

        date = context.get('date') or fields.Datetime.now()
        company_id = context.get('company_id') or self.pool[
            'res.users']._get_company(cr, uid, context=context)
        for id in ids:
            cr.execute("""SELECT rate FROM res_currency_rate
                           WHERE currency_id = %s
                             AND CAST(name AS DATE) <= %s
                             AND (company_id is null
                                 OR company_id = %s)
                        ORDER BY company_id, name desc LIMIT 1""",
                       (id, date, company_id))
            if cr.rowcount:
                res[id] = cr.fetchone()[0]
            else:
                res[id] = 1
        return res

    def _get_conversion_rate(self, cr, uid, from_currency,
                             to_currency, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        if 'date' in ctx.keys():
            if len(ctx['date']) < 11:
                ctx['date'] = ctx['date'] + ' 23:00:00'
        from_currency = self.browse(cr, uid, from_currency.id, context=ctx)
        to_currency = self.browse(cr, uid, to_currency.id, context=ctx)
        return to_currency.rate / from_currency.rate


class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    rate_mex = fields.Float(
        string=_('Rate mexico'),
        digits=(12, 6),
    )

    @api.onchange('rate_mex')
    def _onchange_rate_mex(self):
        if self.rate_mex != 0.00:
            self.rate = 1 / self.rate_mex
        else:
            self.rate = 0.00
