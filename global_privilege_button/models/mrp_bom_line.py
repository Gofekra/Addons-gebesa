# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, _, models
from openerp.exceptions import UserError


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.model
    def create(self, vals):
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_ldm'):
            raise UserError(_('Error!\nYou do not have privileges to Create'
                              ' Material(s) list.\nCheck with your'
                              ' System Administrator.'))
        return super(MrpBomLine, self).create(vals)

    @api.one
    def write(self, vals):
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_ldm'):
            raise UserError(_('Error!\nYou do not have privileges to Modify'
                              ' Material(s) list.\nCheck with your'
                              ' System Administrator.'))
        return super(MrpBomLine, self).write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'global_privilege_button.group_manager_ldm'):
            raise UserError(_('Error!\nYou do not have privileges to Delete'
                              ' Material(s) list.\nCheck with your'
                              ' System Administrator.'))
        return super(MrpBomLine, self).unlink()
