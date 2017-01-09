# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MrpProductionSegment(models.TransientModel):
    _name = 'mrp.production.segment'

    name = fields.Char(
        string='Segment Reference',
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Segment location',
    )

    @api.multi
    def create_segment(self):
        production_obj = self.env['mrp.production']
        segment_obj = self.env['mrp.segment']
        line_obj = self.env['mrp.segment.line']
        active_ids = self._context.get('active_ids', []) or []
        production = production_obj.browse(active_ids)
        segment = segment_obj.create(
            {'name': self.name,
             'location_id': self.location_id.id,
             'date': fields.Datetime.now(),
             'company_id': self.env.user.company_id.id}
        )
        for prod in production:
            if self.location_id != prod.location_dest_id:
                raise ValidationError(_("The production order %s does not \
                                      belong to the selected location") % (
                    prod.name))
            if prod.state in ['confirmed', 'ready']:
                if prod.missing_qty > 0:
                    line_obj.create({
                        'segment_id': segment.id,
                        'mrp_production_id': prod.id,
                        'product_id': prod.product_id.id,
                        'quantity': prod.missing_qty,
                        'sale_name': prod.sale_name,
                    })
        if segment.line_ids:
            segment.state = 'confirm'
        if segment:
            return {
                'name': _('Segment'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mrp.segment',
                'res_id': segment.id,
            }
        return {'type': 'ir.actions.act_window_close'}
