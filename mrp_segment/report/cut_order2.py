# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_cut_order_wood'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_cut_order_wood')
        obj_segment = self.env['mrp.segment']
        segment = obj_segment.browse(self._ids)
        docs = []
        for doc in segment:
            colors = {}
            for line in doc.line_ids:
                production = line.mrp_production_id
                bom_lines = production.bom_id.bom_line_ids
                for bom_line in bom_lines:
                    for detail in bom_line.bom_line_detail_ids:
                        if detail.color_id.name not in colors.keys():
                            colors[detail.color_id.name] = []
                        colors[detail.color_id.name].append({
                            'product': production.product_id,
                            'production': production.name,
                            'qty': production.product_qty,
                            'detail': detail,
                        })

            for color in colors:
                colors[color] = sorted(colors[color],
                                       key=lambda espesor: espesor[
                                       'detail'].thickness)

            docs.append({
                'folio': doc.folio,
                'location': doc.location_id,
                'status': doc.state,
                'name': doc.name,
                'colors': colors
            })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render(
            'mrp_segment.report_cut_order_wood',
            docargs)
