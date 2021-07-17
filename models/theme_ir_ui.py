# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CustomThemeView(models.Model):
    _inherit = 'theme.ir.ui.view'

    customize_show = fields.Boolean("Show As Optional Inherit", default=False)

    def _convert_to_base_model(self, website, **kwargs):
        res = super(CustomThemeView, self)._convert_to_base_model(website=website,
                                                                  **kwargs)
        if res:
            res.update({'customize_show': self.customize_show or False})
        return res
