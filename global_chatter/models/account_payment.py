# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, fields, models


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment', 'mail.thread']
