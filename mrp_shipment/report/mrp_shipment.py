# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ParticularReport(models.AbstractModel):
    _name = 'report.mrp_shipment.report_shipment'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        shipment_obj = self.env['mrp.shipment']
        report = report_obj._get_report_from_name(
            'mrp_shipment.report_shipment')
        docs = shipment_obj.browse(self._ids)
        shipment = {}

        for ship in docs:
            shipment[ship.id] = {}
            for line in ship.line_ids:
                family = line.product_id.family_id.name
                partner = line.partner_id.name
                city = line.city
                if family not in shipment[ship.id].keys():
                    shipment[ship.id][family] = {}
                if partner not in shipment[ship.id][family].keys():
                    shipment[ship.id][family][partner] = {}
                if city not in shipment[ship.id][family][partner].keys():
                    shipment[ship.id][family][partner][city] = []
                shipment[ship.id][family][partner][city].append(line)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': docs,
            'shipment': shipment,
        }
        return report_obj.render('mrp_shipment.report_shipment', docargs)
