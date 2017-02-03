# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ParticularReport(models.AbstractModel):
    _name = 'report.contrarecibo_gebesa.report_contrarecibo'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        contrarecibo_obj = self.env['contrarecibo']
        report = report_obj._get_report_from_name(
            'contrarecibo_gebesa.report_contrarecibo')
        contrarecibo = contrarecibo_obj.browse(self._ids)
        logo = self.env.user.company_id.logo
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': contrarecibo,
            'logo': logo,
        }
        return report_obj.render('contrarecibo_gebesa.report_contrarecibo',
                                 docargs)
