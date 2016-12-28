# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class MrpOperation(models.Model):
    _name = 'mrp.operation'

    code = fields.Char(
        string=_('Code'),
    )

    name = fields.Char(
        string=_('Name'),
    )


class MrpRoutingWorkcenter(models.Model):
    _name = 'mrp.routing.workcenter'
    _inherit = 'mrp.routing.workcenter'

    operation_id = fields.Many2one(
        'mrp.operation',
        string='Operation',
    )
