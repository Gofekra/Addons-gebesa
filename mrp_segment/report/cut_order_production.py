# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_cut_order_production'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_cut_order_production')
        obj_production = self.env['mrp.production']
        mrp_production = obj_production.browse(self._ids)
        docs = []
        for production in mrp_production:
            products = {}
            cut_detail = {}
            cut_line = []
            bom_lines = production.bom_id.bom_line_ids
            bom_line_detail = False
            for bom_line in bom_lines:
                for detail in bom_line.bom_line_detail_ids:
                    bom_line_detail = True
                    production_line = detail.production_line_id.description
                    if production_line not in cut_line:
                        cut_line.append(production_line)
                        cut_detail[production_line] = []
                    add = True
                    for cut in cut_detail[production_line]:
                        if cut['name'] == detail.name and \
                                cut['caliber'] == detail.caliber_id and \
                                cut['width'] == detail.width_cut and \
                                cut['long'] == detail.long_cut:
                            cut['qty'] += detail.quantity * \
                                production.product_qty
                            add = False
                    if add:
                        cut_detail[production_line].append({
                            'name': detail.name,
                            'caliber': detail.caliber_id,
                            'width': detail.width_cut,
                            'long': detail.long_cut,
                            'qty': detail.quantity * production.product_qty
                        })
            if bom_line_detail:
                if production.product_id.id in products.keys():
                    products[production.product_id.id]['product_qty'] += \
                        production.product_qty
                else:
                    products[production.product_id.id] = {
                        'product_name': production.product_id.name,
                        'product_qty': production.product_qty,
                        'product_code': production.product_id.default_code,
                    }
            for cut_d in cut_detail:
                cut_detail[cut_d] = sorted(cut_detail[cut_d],
                                           key=lambda cut: cut['long'])
                cut_detail[cut_d] = sorted(cut_detail[cut_d],
                                           key=lambda cut: cut['width'])
                cut_detail[cut_d] = sorted(cut_detail[cut_d],
                                           key=lambda cut: cut[
                                           'caliber'].key_caliber)
                cut_detail[cut_d] = sorted(cut_detail[cut_d],
                                           key=lambda cut: cut['name'])

            docs.append({
                'name': production.name,
                'folio': None,
                'products': products,
                'cut_line': cut_line,
                'cut_detail': cut_detail,
            })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render(
            'mrp_segment.report_cut_order_production',
            docargs)
