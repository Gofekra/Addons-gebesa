# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class FactoringSupplier(models.Model):
    _name = 'factoring.supplier'
    _inherit = ['mail.thread']
    _description = "Factoring Supplier"
    _order = 'reference asc'
    _rec_name = 'reference'

    reference = fields.Char(
        string=_('Reference'),
        size=250,
        track_visibility='onchange')

    partner_id = fields.Many2one(
        'res.partner',
        string=_(u'Supplier'),
        track_visibility='onchange')

    journal_id = fields.Many2one(
        'account.journal',
        string=_(u'Bank'),
        domain="[('type', 'in', ('bank','cash'))]",
        track_visibility='onchange')

    company_id = fields.Many2one(
        'res.company',
        string=_(u'Company'),
        default=lambda self: self.env['res.company']._company_default_get(
            'factoring.supplier'),
        track_visibility='always')

    date = fields.Date(
        string=_(u'Date'),
        default=fields.Date.today,
        track_visibility='always')

    invoice_ids = fields.Many2many(
        'account.invoice',
        string=_(u'Supplier Invoices'),
        track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        string=_(u'Status'),
        track_visibility='onchange',
        default='draft')

    date_bank = fields.Date(
        string=_(u'Payment Date the Bank'),
        track_visibility='always')

    _sql_constraints = [
        ('reference_uniq', 'unique (reference)',
         'This field must be unique!')
    ]

    def integrated_factoring(self, _cr, _uid, _ids, _context=None):
        ids = isinstance(_ids, (int, long)) and [_ids] or _ids
        inv_obj = self.pool.get('account.invoice')
        res = {}

        int_brw = self.browse(_cr, _uid, ids[0], context=_context)
        for inv_brw in int_brw.invoice_ids:
            inv_obj.write(_cr, _uid, [
                          inv_brw.id], {'factoring_supplier_id': int_brw.id},
                          context=_context)

        self.write(_cr, _uid, [int_brw.id], {'state': 'done'},
                   context=_context)

        return res
