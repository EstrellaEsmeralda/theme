# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.


from odoo import models, api


class ThemeNew(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_scita_post_copy(self, mod):
        self.disable_view_customize('website_sale_wishlist.product_add_to_wishlist')
        self.disable_view_customize('website_sale.product_quantity')
        self.disable_view_customize('website_sale_comparison.product_attributes_body')
        self.disable_view_customize('website_sale.product_comment')
        self.disable_view_customize('website_sale.recommended_products')
        self.disable_view_customize('website_sale.product_variants')
        self.disable_view_customize('website_sale.ecom_show_extra_fields')
        # other template
        self.disable_view_customize('website_sale.search_count_box')
        self.disable_view_customize('website_sale.products_list_view')
        self.disable_view_customize('website_sale.add_grid_or_list_option')
        self.disable_view_customize('website_sale.products_attributes')
        self.disable_view_customize('website_sale.sort')
        self.disable_view_customize('website_sale.products_categories')
        self.disable_view_customize('website_sale.products_description')
        self.disable_view_customize('website_sale_comparison.add_to_compare')
        self.disable_view_customize('website_sale.products_add_to_cart')
        self.disable_view_customize('website_sale_wishlist.add_to_wishlist')
        self.disable_view_customize('website_sale.product_custom_text')
        self.disable_view_customize('website_sale.product_picture_magnify_auto')
        self.disable_view_customize('website_sale.products_images_full')
        self.disable_view('website_sale_comparison.product_add_to_compare')
        self.enable_view('website.header_hoverable_dropdown')


    @api.model
    def _toggle_view_customize(self, xml_id, active):
        obj = self.env.ref(xml_id)
        website = self.env['website'].get_current_website()
        if obj._name == 'theme.ir.ui.view':
            obj = obj.with_context(active_test=False)
            obj = obj.copy_ids.filtered(lambda x: x.website_id == website)
        else:
            View = self.env['ir.ui.view'].with_context(active_test=False)
            has_specific = obj.key and View.search_count([
                ('key', '=', obj.key),
                ('website_id', '=', website.id)
            ]) >= 1
            if not has_specific and active == obj.active and active == obj.customize_show:
                return
        obj.write({'active': active})
        obj.write({'customize_show': active})

    @api.model
    def enable_view_customize(self, xml_id):
        self._toggle_view_customize(xml_id, True)

    @api.model
    def disable_view_customize(self, xml_id):
        self._toggle_view_customize(xml_id, False)
