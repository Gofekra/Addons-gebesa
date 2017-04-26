# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )

    review = fields.Selection([
        ('no_review', _('No Review')),
        ('yes_review', _('Review'))],
        string=_('Change'),
        default='no_review')

    @api.multi
    def action_review(self):
        for picking in self:
            if picking.review == 'no_review':
                if self._uid == self.create_uid.id:
                    raise UserError(_("You can not modify this picking"))
                self.write({'review': 'yes_review'})
            else:
                raise UserError(_("Already reviewed"))
        return True

    @api.multi
    def do_transfer(self):
        for sp in self:
            ware_var = sp.location_id.stock_warehouse_id
            ware_dest_var = sp.location_dest_id.stock_warehouse_id
            if ware_var and ware_dest_var:
                if ware_dest_var != ware_var:
                    if sp.review == 'no_review':
                        raise UserError(_("Needs to be reviewed"))
        return super(StockPicking, self).do_transfer()


class StockMove(models.Model):
    _inherit = 'stock.move'

    related_segment = fields.Char(
        string='Relatad Segment',
        default='',
    )
