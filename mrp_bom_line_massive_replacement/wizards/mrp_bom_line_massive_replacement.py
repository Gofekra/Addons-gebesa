# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountingReport(models.TransientModel):
    _name = "mrp.bom.line.massive.replacement"

    product_id = fields.Many2one(
        'product.product',
        string='Product origin',
    )
    new_product_id = fields.Many2one(
        'product.product',
        string='New product',
    )

    @api.multi
    def process(self):
        bom_line_obj = self.env['mrp.bom.line']
        ## ---> Set BreakPoint
        import pdb;
        pdb.set_trace()
        for replacement in self:
            bom_line = bom_line_obj.search(
                [('product_id', '=', replacement.product_id.id)])
            for line in bom_line:
                line.product_id = replacement.new_product_id.id
