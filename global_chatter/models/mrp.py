# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MrpBom(models.Model):
    _name = 'mrp.bom'
    _inherit = ['mrp.bom', 'message.post.show.all']


class MrpBomLine(models.Model):
    _name = 'mrp.bom.line'
    _inherit = ['mrp.bom.line', 'message.post.show.all']


class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'message.post.show.all']


class MrpShipment(models.Model):
    _name = 'mrp.shipment'
    _inherit = ['mrp.shipment', 'message.post.show.all']
