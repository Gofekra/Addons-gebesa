# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.report_price_list.report_price_modulares'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'report_price_list.report_price_modulares')
        line_obj = self.env['product.line']
        group_obj = self.env['product.group']
        product_obj = self.env['product.template']
        order_key = []
        order_key_len = []

        pagina = {}

        pagina[1] = {}
        line = line_obj.search([('name', '=', 'Synergy'),
                                ('code', '=', 'GES')])
        group = group_obj.search([('name', '=', 'Mamparas')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('name', 'not like', "% Mixta %"),
                                      ('is_line', '=', True)],
                                     order="height, length")
        for prod in product:
            if prod.height in pagina[1].keys():
                pagina[1][prod.height].append(prod)
            else:
                order_key.append(prod.height)
                pagina[1][prod.height] = []
                pagina[1][prod.height].append(prod)

        pagina[2] = {}
        group = group_obj.search([('name', '=', 'Postes')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('is_line', '=', True)],
                                     order="height")
        pagina[2]['postes'] = []
        for prod in product:
            pagina[2]['postes'].append(prod)
        group = group_obj.search([('name', '=', 'Remates')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('is_line', '=', True)],
                                     order="height")
        pagina[2]['Tapa1'] = []
        pagina[2]['Tapa2'] = []
        for prod in product:
            if 'Remate' in str(prod.name):
                pagina[2]['Tapa1'].append(prod)
            else:
                pagina[2]['Tapa2'].append(prod)

        pagina[3] = {}
        pagina[4] = {}
        pagina[4]['Inf'] = {}
        pagina[4]['Sup'] = {}
        pagina[5] = {}
        pagina[5]['Sup'] = {}
        line = line_obj.search([('name', '=', 'Optimus'),
                                ('code', '=', 'GEO')])
        group = group_obj.search([('name', '=', 'Mamparas')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('is_line', '=', True)],
                                     order="height, length")
        for prod in product:
            if 'Estructura' in str(prod.name):
                if prod.height in pagina[3].keys():
                    pagina[3][prod.height].append(prod)
                else:
                    pagina[3][prod.height] = []
                    pagina[3][prod.height].append(prod)
            else:
                if 'CN' in str(prod.name):
                    key = 'CN'
                if 'BP' in str(prod.name):
                    key = 'BP'
                if 'Tapiz' in str(prod.name):
                    key = 'Tapiz'
                if 'Pintarron' in str(prod.name):
                    key = 'Pintarron'
                if 'Inf' in str(prod.name):
                    if prod.length not in pagina[4]['Inf'].keys():
                        order_key_len.append(prod.length)
                        pagina[4]['Inf'][prod.length] = {}
                    pagina[4]['Inf'][prod.length][key] = prod
                if 'Sup' in str(prod.name):
                    if 3 >= len(pagina[4]['Sup'].keys() + pagina[5][
                            'Sup'].keys()):
                        if prod.height not in pagina[4]['Sup'].keys():
                            if 3 == len(pagina[4]['Sup'].keys()):
                                pagina[5]['Sup'][prod.height] = {}
                                pagina[5]['Sup'][prod.height][prod.length] = {}
                                pagina[5]['Sup'][prod.height][prod.length][
                                    key] = prod
                                continue
                            else:
                                pagina[4]['Sup'][prod.height] = {}
                        if prod.length not in pagina[4]['Sup'][
                                prod.height].keys():
                            pagina[4]['Sup'][prod.height][prod.length] = {}
                        pagina[4]['Sup'][prod.height][prod.length][key] = prod
                    else:
                        if prod.height not in pagina[5]['Sup'].keys():
                            pagina[5]['Sup'][prod.height] = {}
                        if prod.length not in pagina[5]['Sup'][
                                prod.height].keys():
                            pagina[5]['Sup'][prod.height][prod.length] = {}
                        pagina[5]['Sup'][prod.height][prod.length][key] = prod

        pagina[6] = {}
        group = group_obj.search([('name', '=', 'Postes')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('is_line', '=', True)],
                                     order="height, vias")
        pagina[6]['postes'] = {}
        for prod in product:
            if prod.height not in pagina[6]['postes'].keys():
                pagina[6]['postes'][prod.height] = {}
            pagina[6]['postes'][prod.height][prod.vias] = prod
        group = group_obj.search([('name', '=', 'Remates')])
        product = product_obj.search([('group_id', '=', group.id),
                                      ('line_id', '=', line.id),
                                      ('is_line', '=', True)],
                                     order="height")
        pagina[6]['Tapa1'] = []
        pagina[6]['Tapa2'] = []
        for prod in product:
            if 'Remate' in str(prod.name):
                pagina[6]['Tapa1'].append(prod)
            else:
                pagina[6]['Tapa2'].append(prod)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env.user,
            'langu': self._context['lang'],
            'pagina': pagina,
            'order_key': order_key,
            'order_key_len': order_key_len,
        }
        return report_obj.render(
            'report_price_list.report_price_modulares',
            docargs)
