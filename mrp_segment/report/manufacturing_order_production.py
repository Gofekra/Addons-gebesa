# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_segment.report_manufacturing_order_production'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'mrp_segment.report_manufacturing_order_production')
        obj_production = self.env['mrp.production']
        production = obj_production.browse(self._ids)
        docs = []
        for doc in production:
            lines = []
            mp_lines = []
            groups = {}
            mp_groups = {}
            products = {}
            mp_products = {}
            pedidos = []
            fabricacion = doc.name
            line_id = doc.product_id.line_id
            group_id = doc.product_id.group_id
            if line_id not in lines:
                lines.append(line_id)
                groups[line_id.id] = []
            if group_id not in groups[line_id.id]:
                groups[line_id.id].append(group_id)
                products[str(line_id.id) + '-' + str(group_id.id)] = []
            products[str(line_id.id) + '-' + str(group_id.id)].append({
                'id': doc.product_id.id,
                'product_code': doc.product_id.default_code,
                'product_name': doc.product_id.name,
                'standard_cost': doc.product_id.standard_price,
                'product_qty': doc.product_qty,
            })
            if doc.sale_id not in pedidos:
                pedidos.append(doc.sale_id)
            product_lines_ids = sorted(
                doc.product_lines,
                key=lambda line: line.id)

            for prod_line in product_lines_ids:
                line_id = prod_line.product_id.line_id
                group_id = prod_line.product_id.group_id
                if line_id not in mp_lines:
                    mp_lines.append(line_id)
                    mp_groups[line_id.id] = []
                if group_id not in mp_groups[line_id.id]:
                    mp_groups[line_id.id].append(group_id)
                    mp_products[str(line_id.id) + '-' + str(group_id.id)] = []
                add = True

                for prod in mp_products[
                        str(line_id.id) + '-' + str(group_id.id)]:
                    if prod_line.product_id.id == prod['id']:
                        prod['product_qty'] = prod[
                            'product_qty'] + prod_line.product_qty
                        prod['standard_cost'] = prod_line.standard_cost
                        add = False
                if add:
                    mp_products[
                        str(line_id.id) + '-' + str(group_id.id)].append({
                            'id': prod_line.product_id.id,
                            'location': prod_line.location_id.name,
                            'product_code': prod_line.product_id.default_code,
                            'product_name': prod_line.product_id.name,
                            'standard_cost': prod_line.standard_cost,
                            'product_qty': prod_line.product_qty,
                            'uom': prod_line.product_uom.name,
                        })

            docs.append({
                'date': doc.date_planned,
                'state': doc.state,
                'folio': doc.name,
                'location_dest_id': doc.location_dest_id.name,
                'lines': lines,
                'groups': groups,
                'products': products,
                'pedidos': pedidos,
                'mp_lines': mp_lines,
                'mp_groups': mp_groups,
                'mp_products': mp_products,
                'fabricacion': fabricacion,
            })

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render(
            'mrp_segment.report_manufacturing_order_production',
            docargs)
