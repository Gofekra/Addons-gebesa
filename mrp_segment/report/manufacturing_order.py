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
        lines = []
        groups = {}
        products = {}
        pedidos = []
        for line in segment.line_ids:
            line_id = line.product_id.line_id
            group_id = line.product_id.group_id
            if line_id.name not in lines:
                lines.append(line_id.name)
                groups[line_id.name] = []
            if group_id.name not in groups[line_id.name]:
                groups[line_id.name].append(group_id.name)
                products[line_id.name + '-' + group_id.name] = []
            products[line_id.name + '-' + group_id.name].append(line)

        docargs = {
            'lines': lines,
            'groups': groups,
            'products': products,
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': segment,
        }
        # obj_line = self.env['product.line']
        # obj_product = self.env['product.template']
        # docs = {}
        # lines_id = obj_line.search([('active', '=', True)],
        #                            order='code')
        # lines = []
        # for line in lines_id:
        #     product_tamplate = obj_product.search([('pricelist', '=', True),
        #                                            ('is_line', '=', True),
        #                                            ('line_id', '=', line.id)],
        #                                           order=None)
        #     if product_tamplate:
        #         lines.append(line.id)
        #         docs[line.name] = []
        #         page = []
        #         count = 0
        #         for product in product_tamplate:
        #             if count == 5:
        #                 docs[line.name].append(page)
        #                 page = []
        #                 count = 0
        #             page.append(product)
        #             count += 1
        #         if page:
        #             docs[line.name].append(page)

        # logo = self.env.user.company_id.logo
        # lines_id = obj_line.search([('id', 'in', lines)], order='code')
        # docargs = {
        #     'doc_ids': self._ids,
        #     'doc_model': report.model,
        #     'docs': docs,
        #     'logo': logo,
        #     'lines_id': lines_id,
        #     'langu': self._context['lang']
        # }
        return report_obj.render(
            'mrp_segment.report_manufacturing_order',
            docargs)
