# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.stock_picking_batch.report_picking_batch'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        batch_picking_obj = self.env['stock.batch.picking']
        report = report_obj._get_report_from_name(
            'stock_picking_batch.report_picking_batch')
        bat_pick = {}
        picking = {}
        batch_picking = batch_picking_obj.browse(self._ids)
        for batch in batch_picking:
            bat_pick[batch.id] = {}
            picking[batch.id] = []
            for pick in batch.picking_ids:
                if pick not in picking[batch.id]:
                    picking[batch.id].append(pick)
                loc = pick.location_id.name
                loc_des = pick.location_dest_id.name
                if loc not in bat_pick[batch.id].keys():
                    bat_pick[batch.id][loc] = {}
                if loc_des not in bat_pick[batch.id][
                        loc].keys():
                    bat_pick[batch.id][loc][loc_des] = {}
                for pack in pick.pack_operation_product_ids:
                    prod = pack.product_id
                    if prod.id not in bat_pick[batch.id][
                            loc][loc_des].keys():
                        bat_pick[batch.id][loc][loc_des][prod.id] = {}
                        bat_pick[batch.id][loc][loc_des][prod.id][
                            'product'] = prod
                        bat_pick[batch.id][loc][loc_des][prod.id][
                            'carrier'] = [pack.package_id]
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['qty'] = pack.product_qty
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['pick'] = [pick]
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['so'] = [pick.sale_id]
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['re'] = [pick.related_segment]
                    else:
                        bat_pick[batch.id][loc][loc_des][prod.id][
                            'carrier'].append(pack.package_id)
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['qty'] += pack.product_qty
                        bat_pick[batch.id][loc][loc_des][
                            prod.id]['pick'].append(pick)
                        if pick.sale_id not in bat_pick[batch.id][loc][
                                loc_des][prod.id]['so']:
                            bat_pick[batch.id][loc][loc_des][
                                prod.id]['so'].append(pick.sale_id)
                        if pick.related_segment not in bat_pick[batch.id][loc][
                                loc_des][prod.id]['re']:
                            bat_pick[batch.id][loc][loc_des][
                                prod.id]['re'].append(pick.related_segment)
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': batch_picking,
            'bat_pick': bat_pick,
            'picking': picking,
        }
        return report_obj.render('stock_picking_batch.report_picking_batch',
                                 docargs)
