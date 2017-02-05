# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_manufacturing_order'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_manufacturing_order')
        obj_segment = self.env['mrp.segment']
        segment = obj_segment.browse(self._ids)
        docs = []
        for doc in segment:
            lines = []
            mp_lines = []
            groups = {}
            mp_groups = {}
            products = {}
            mp_products = {}
            pedidos = []
            lines_ids = sorted(doc.line_ids,
                               key=lambda line: line.mrp_production_id.id)
            for line in lines_ids:
                line_id = line.product_id.line_id
                group_id = line.product_id.group_id
                if line_id not in lines:
                    lines.append(line_id)
                    groups[line_id.name] = []
                if group_id not in groups[line_id.name]:
                    groups[line_id.name].append(group_id)
                    products[line_id.name + '-' + group_id.name] = []
                add = True
                for prod in products[line_id.name + '-' + group_id.name]:
                    if line.product_id.id == prod['id']:
                        prod['product_qty'] = prod[
                            'product_qty'] + line.product_qty
                        prod['standard_cost'] = line.standard_cost
                        add = False
                if add:
                    products[line_id.name + '-' + group_id.name].append({
                        'id': line.product_id.id,
                        'product_code': line.product_id.default_code,
                        'product_name': line.product_id.name,
                        'standard_cost': line.standard_cost,
                        'product_qty': line.product_qty,
                    })
                if line.mrp_production_id.sale_id not in pedidos:
                    pedidos.append(line.mrp_production_id.sale_id)

            product_lines_ids = sorted(
                doc.product_lines_ids,
                key=lambda line: line.id)
            for prod_line in product_lines_ids:
                line_id = prod_line.product_id.line_id
                group_id = prod_line.product_id.group_id
                if line_id not in mp_lines:
                    mp_lines.append(line_id)
                    mp_groups[line_id.name] = []
                if group_id not in mp_groups[line_id.name]:
                    mp_groups[line_id.name].append(group_id)
                    mp_products[line_id.name + '-' + group_id.name] = []
                add = True

                for prod in mp_products[line_id.name + '-' + group_id.name]:
                    if prod_line.product_id.id == prod['id']:
                        prod['product_qty'] = prod[
                            'product_qty'] + prod_line.product_qty
                        prod['standard_cost'] = prod_line.standard_cost
                        add = False
                if add:
                    mp_products[line_id.name + '-' + group_id.name].append({
                        'id': prod_line.product_id.id,
                        'location': prod_line.location_id.name,
                        'product_code': prod_line.product_id.default_code,
                        'product_name': prod_line.product_id.name,
                        'standard_cost': prod_line.standard_cost,
                        'product_qty': prod_line.product_qty,
                        'uom': prod_line.product_uom.name,
                    })

            docs.append({
                'date': doc.date,
                'state': doc.state,
                'folio': doc.folio,
                'location_dest_id': doc.location_id.name,
                'lines': lines,
                'groups': groups,
                'products': products,
                'pedidos': pedidos,
                'mp_lines': mp_lines,
                'mp_groups': mp_groups,
                'mp_products': mp_products,
            })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render(
            'mrp_segment.report_manufacturing_order',
            docargs)
