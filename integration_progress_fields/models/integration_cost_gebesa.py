# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class IntegrationCostGebesa(models.Model):
    _inherit = 'integration.cost.gebesa'

    concat_progress = fields.Text(
        string=_(u'concatenated to progress'),
    )
