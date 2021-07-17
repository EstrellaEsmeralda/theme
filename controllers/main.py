# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.
import re
import math
import json
import os
from werkzeug.exceptions import Forbidden, NotFound
from odoo import http, SUPERUSER_ID, fields
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute


class ScitaSliderSettings(http.Controller):

    def get_blog_data(self, slider_type):
        slider_header = request.env['blog.slider.config'].sudo().search(
            [('id', '=', int(slider_type))])
        values = {
            'slider_header': slider_header,
            'blog_slider_details': slider_header.collections_blog_post,
        }
        return values

    def get_categories_data(self, slider_id):
        slider_header = request.env['category.slider.config'].sudo().search(
            [('id', '=', int(slider_id))])
        values = {
            'slider_header': slider_header
        }
        values.update({
            'slider_details': slider_header.collections_category,
        })
        return values

    def get_clients_data(self):
        client_data = request.env['res.partner'].sudo().search(
            [('add_to_slider', '=', True), ('website_published', '=', True)])
        values = {
            'client_slider_details': client_data,
        }
        return values

    def get_teams_data(self):
        employee = request.env['hr.employee'].sudo().search(
            [('include_inourteam', '=', 'True')])
        values = {
            'employee': employee,
        }
        return values

    @http.route(['/theme_scita/blog_get_options'], type='json', auth="public", website=True)
    def scita_get_slider_options(self):
        slider_options = []
        option = request.env['blog.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_scita/blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def scita_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.theme_scita_blog_slider_view")._render(values)

    @http.route(['/theme_scita/health_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def health_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.health_blog_slider_view")._render(values)

    @http.route(['/theme_scita/second_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def second_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_2_slider_view")._render(values)

    @http.route(['/theme_scita/third_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def third_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_3_slider_view")._render(values)

    @http.route(['/theme_scita/six_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def six_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_6_slider_view")._render(values)

    @http.route(['/theme_scita/forth_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def forth_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_4_slider_view")._render(values)

    @http.route(['/theme_scita/fifth_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def fifth_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_5_slider_view")._render(values)

    @http.route(['/theme_scita/seven_blog_get_dynamic_slider'], type='http', auth='public', website=True)
    def seven_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.render("theme_scita.scita_blog_7_slider_view", values)

    @http.route(['/theme_scita/eight_blog_get_dynamic_slider'], type='json', auth='public', website=True)
    def eight_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            values = self.get_blog_data(post.get('slider-type'))
            return request.website.viewref("theme_scita.scita_blog_8_slider_view")._render(values)

    @http.route(['/theme_scita/blog_image_effect_config'], type='json', auth='public', website=True)
    def scita_product_image_dynamic_slider(self, **post):
        slider_data = request.env['blog.slider.config'].search(
            [('id', '=', int(post.get('slider_type')))])
        values = {
            's_id': str(slider_data.no_of_counts) + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    # for Client slider
    @http.route(['/theme_scita/get_clients_dynamically_slider'], type='json', auth='public', website=True)
    def get_clients_dynamically_slider(self, **post):
        values = self.get_clients_data()
        return request.website.viewref("theme_scita.theme_scita_client_slider_view")._render(values)

    @http.route(['/theme_scita/second_get_clients_dynamically_slider'], type='json', auth='public', website=True)
    def second_get_clients_dynamically_slider(self, **post):
        values = self.get_clients_data()
        return request.website.viewref("theme_scita.second_client_slider_view")._render(values)

    @http.route(['/theme_scita/third_get_clients_dynamically_slider'], type='json', auth='public', website=True)
    def third_get_clients_dynamically_slider(self, **post):
        values = self.get_clients_data()
        return request.website.viewref("theme_scita.third_client_slider_view")._render(values)

    # our team

    @http.route(['/biztech_emp_data_one/employee_data'], type='json', auth='public', website=True)
    def get_team_one_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.it_our_team_view")._render(values)

    @http.route(['/biztech_emp_data_two/employee_data'], type='json', auth='public', website=True)
    def get_team_two_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_2_view")._render(values)

    @http.route(['/biztech_emp_data_three/employee_data'], type='json', auth='public', website=True)
    def get_team_three_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_3_view")._render(values)

    @http.route(['/biztech_emp_data_four/employee_data'], type='json', auth='public', website=True)
    def get_team_four_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_4_view")._render(values)

    @http.route(['/biztech_emp_data_five/employee_data'], type='json', auth='public', website=True)
    def get_team_five_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_5_view")._render(values)

    @http.route(['/biztech_emp_data_six/employee_data'], type='json', auth='public', website=True)
    def get_team_six_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_6_view")._render(values)

    @http.route(['/biztech_emp_data_seven/employee_data'], type='json', auth='public', website=True)
    def get_team_seven_dynamically_slider(self, **post):
        values = self.get_teams_data()
        return request.website.viewref("theme_scita.our_team_varient_7_view")._render(values)

    # For Category slider

    @http.route(['/theme_scita/category_get_options'], type='json', auth="public", website=True)
    def category_get_slider_options(self):
        slider_options = []
        option = request.env['category.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_scita/category_get_dynamic_slider'], type='json', auth='public', website=True)
    def category_get_dynamic_slider(self, **post):
        if post.get('slider-id'):
            values = self.get_categories_data(post.get('slider-id'))
            return request.website.viewref("theme_scita.theme_scita_cat_slider_view")._render(values)

    @http.route(['/theme_scita/second_get_dynamic_cat_slider'], type='json', auth='public', website=True)
    def second_get_dynamic_cat_slider(self, **post):
        if post.get('slider-id'):
            values = self.get_categories_data(post.get('slider-id'))
            return request.website.viewref("theme_scita.second_cat_slider_view")._render(values)

    @http.route(['/theme_scita/category_slider_3'], type='json', auth='public', website=True)
    def category_slider_value(self, **post):
        if post.get('slider-id'):
            values = self.get_categories_data(post.get('slider-id'))
            return request.website.viewref("theme_scita.theme_scita_category_slider_3_view")._render(values)

    @http.route(['/theme_scita/category_slider_4'], type='json', auth='public', website=True)
    def category_slider_four(self, **post):
        if post.get('slider-id'):
            values = self.get_categories_data(post.get('slider-id'))
            return request.website.viewref("theme_scita.theme_scita_category_slider_4_view")._render(values)

    @http.route(['/theme_scita/scita_image_effect_config'], type='json', auth='public', website=True)
    def category_image_dynamic_slider(self, **post):
        slider_data = request.env['category.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': slider_data.name.lower().replace(' ', '-') + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    # For Product slider
    @http.route(['/theme_scita/product_get_options'], type='json', auth="public", website=True)
    def product_get_slider_options(self):
        slider_options = []
        option = request.env['product.slider.config'].search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_scita/product_get_dynamic_slider'], type='json', auth='public', website=True)
    def product_get_dynamic_slider(self, **post):
        if post.get('slider-id'):
            slider_header = request.env['product.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-id')))])
            values = {
                'slider_header': slider_header
            }
            values.update({
                'slider_details': slider_header.collections_products,
            })
            return request.website.viewref("theme_scita.theme_scita_product_slider_view")._render(values)

    @http.route(['/theme_scita/product_image_effect_config'], type='json', auth='public', website=True)
    def product_image_dynamic_slider(self, **post):
        slider_data = request.env['product.slider.config'].search(
            [('id', '=', int(post.get('slider_id')))])
        values = {
            's_id': slider_data.name.lower().replace(' ', '-') + '-' + str(slider_data.id),
            'counts': slider_data.no_of_counts,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
        }
        return values

    # For multi product slider
    @http.route(['/theme_scita/product_multi_get_options'], type='json', auth="public", website=True)
    def product_multi_get_slider_options(self):
        slider_options = []
        option = request.env['multi.slider.config'].sudo().search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/retial/product_multi_get_dynamic_slider'], type='json', auth='public', website=True)
    def retail_multi_get_dynamic_slider(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['multi.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])

            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(
                SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price): return pool['res.currency']._convert(
                price, from_currency, to_currency, fields.Date.today())
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency,
            }
            return request.website.viewref("theme_scita.scita_multi_cat_slider_view")._render(values)

    @http.route(['/fashion/fashion_product_multi_get_dynamic_slider'], type='json', auth='public', website=True)
    def fashion_multi_get_dynamic_slider(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['multi.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])

            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(
                SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price): return pool['res.currency']._convert(
                price, from_currency, to_currency, fields.Date.today())
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency,
            }
            return request.website.viewref("theme_scita.fashion_multi_cat_slider_view")._render(values)

    @http.route(['/theme_scita/product_multi_image_effect_config'], type='json', auth='public', website=True)
    def product_multi_product_image_dynamic_slider(self, **post):
        slider_data = request.env['multi.slider.config'].sudo().search(
            [('id', '=', int(post.get('slider_type')))])
        values = {
            's_id': slider_data.no_of_collection + '-' + str(slider_data.id),
            'counts': slider_data.no_of_collection,
            'auto_rotate': slider_data.auto_rotate,
            'auto_play_time': slider_data.sliding_speed,
            'rating_enable': slider_data.is_rating_enable
        }
        return values

    # Multi image gallery
    @http.route(['/theme_scita/scita_multi_image_thumbnail_config'], type='json', auth="public", website=True)
    def get_multi_image_effect_config(self):

        cur_website = request.website
        values = {
            'no_extra_options': cur_website.no_extra_options,
            'interval_play': cur_website.interval_play,
            'enable_disable_text': cur_website.enable_disable_text,
            'color_opt_thumbnail': cur_website.color_opt_thumbnail,
            'theme_panel_position': cur_website.thumbnail_panel_position,
            'change_thumbnail_size': cur_website.change_thumbnail_size,
            'thumb_height': cur_website.thumb_height,
            'thumb_width': cur_website.thumb_width,
        }
        return values
    # For new brand snippet and product and category snippet

    @http.route(['/theme_scita/brand_get_options'], type='json', auth="public", website=True)
    def custom_brand_get_options(self):
        slider_options = []
        option = request.env['brand.snippet.config'].sudo().search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_scita/custom_pro_get_dynamic_slider'], type='json', auth='public', website=True)
    def custom_pro_get_dynamic_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['product.category.img.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header
            }
            if slider_header.prod_cat_type == 'product':
                values.update(
                    {'slider_details': slider_header.collections_product})
            if slider_header.prod_cat_type == 'category':
                values.update(
                    {'slider_details': slider_header.collections_category})
            values.update({'slider_type': slider_header.prod_cat_type})
            return request.website.viewref("theme_scita.custom_scita_cat_slider_view")._render(values)

    @http.route(['/theme_scita/custom_get_brand_slider'], type='json', auth='public', website=True)
    def custom_get_brand_slider(self, **post):
        keep = QueryURL('/theme_scita/custom_get_brand_slider', brand_id=[])
        if post.get('slider-type'):
            slider_header = request.env['brand.snippet.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'website_brands': slider_header.collections_brands
            }
        return request.website.viewref("theme_scita.custom_scita_brand_slider_view")._render(values)

    @http.route(['/theme_scita/pro_get_options'], type='json', auth="public", website=True)
    def get_slider_options(self):
        slider_options = []
        option = request.env['product.category.img.slider.config'].sudo().search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    # Zipcode delivery status
    @http.route(['/shop/zipcode'], type='json', auth="public", website=True)
    def scita_get_delivery_zipcode(self, zip_code, **post):
        if zip_code:
            zip_obj = request.env['delivery.zipcode'].search(
                [('name', '=', zip_code)])
            if zip_obj.id:
                return {'status': True}
            else:
                return {'status': False}
        else:
            return {'zip': 'notavailable'}

    @http.route(['/product_column_five'], type='json', auth='public', website=True)
    def get_product_column_five(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['product.snippet.configuration'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(
                SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price): return pool['res.currency']._convert(
                price, from_currency, to_currency, fields.Date.today())
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency,
                'products': slider_header.collection_of_products
            }
            return request.website.viewref("theme_scita.sct_product_snippet_1_view")._render(values)

    @http.route(['/product/product_snippet_data_two'], type='json', auth='public', website=True)
    def product_snippet_data_two(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['product.snippet.configuration'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])

            context.update({'pricelist': pricelist.id})
            from_currency = pool['res.users'].sudo().browse(
                SUPERUSER_ID).company_id.currency_id
            to_currency = pricelist.currency_id

            def compute_currency(price): return pool['res.currency']._convert(
                price, from_currency, to_currency, fields.Date.today())
            values = {
                'slider_details': slider_header,
                'slider_header': slider_header,
                'compute_currency': compute_currency,
                'products': slider_header.collection_of_products
            }
            return request.website.viewref("theme_scita.sct_product_snippet_2_view")._render(values)

    @http.route(['/theme_scita/product_configuration'], type='json', auth="public", website=True)
    def snippet_get_product_configuration(self):
        slider_options = []
        option = request.env['product.snippet.configuration'].sudo().search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/deals-of-the-day'], type="http", auth="public", website=True)
    def products(self, **post):
        product = request.env['product.template'].search([('deal_product', '=', True)])
        values = {'deal_products': product}
        return request.render("theme_scita.biz_deal_page", values)


class ScitaShop(WebsiteSale):

    @http.route(['/shop/pager_selection/<model("product.per.page.no"):pl_id>'], type='http', auth="public", website=True)
    def product_page_change(self, pl_id, **post):
        request.session['default_paging_no'] = pl_id.name
        main.PPG = pl_id.name
        return request.redirect(request.httprequest.referrer or '/shop')

    @http.route('/shop/products/recently_viewed', type='json', auth='public', website=True)
    def products_recently_viewed(self, **kwargs):
        if request.env['website'].sudo().get_current_website().theme_id.name == 'theme_scita':
            return self._get_scita_products_recently_viewed()
        else:
            return self._get_products_recently_viewed()

    def _get_scita_products_recently_viewed(self):
        max_number_of_product_for_carousel = 12
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if visitor:
            excluded_products = request.website.sale_get_order().mapped(
                'order_line.product_id.id')
            products = request.env['website.track'].sudo().read_group(
                [('visitor_id', '=', visitor.id), ('product_id', '!=', False),
                 ('product_id', 'not in', excluded_products)],
                ['product_id', 'visit_datetime:max'], ['product_id'], limit=max_number_of_product_for_carousel, orderby='visit_datetime DESC')
            products_ids = [product['product_id'][0] for product in products]
            if products_ids:
                viewed_products = request.env['product.product'].browse(
                    products_ids)

                FieldMonetary = request.env['ir.qweb.field.monetary']
                monetary_options = {
                    'display_currency': request.website.get_current_pricelist().currency_id,
                }
                rating = request.website.viewref(
                    'theme_scita.theme_scita_rating').active
                res = {'products': []}
                for product in viewed_products:
                    combination_info = product._get_combination_info_variant()
                    res_product = product.read(
                        ['id', 'name', 'website_url'])[0]
                    res_product.update(combination_info)
                    res_product['price'] = FieldMonetary.value_to_html(
                        res_product['price'], monetary_options)
                    if rating:
                        res_product['rating'] = request.env["ir.ui.view"]._render_template('portal_rating.rating_widget_stars_static', values={
                            'rating_avg': product.rating_avg,
                            'rating_count': product.rating_count,
                        })
                    res['products'].append(res_product)

                return res
        return {}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>''',
        '''/shop/brands'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, brands=None, **post):
        if request.env['website'].sudo().get_current_website().theme_id.name == 'theme_scita':
            add_qty = int(post.get('add_qty', 1))
            values = {}
            Category = request.env['product.public.category']
            if category:
                category = Category.search(
                    [('id', '=', int(category))], limit=1)
                if not category or not category.can_access_from_current_website():
                    raise NotFound()
            else:
                category = Category
            if brands:
                req_ctx = request.context.copy()
                req_ctx.setdefault('brand_id', int(brands))
                request.context = req_ctx
            page_no = request.env['product.per.page.no'].sudo().search(
                [('set_default_check', '=', True)])
            if page_no:
                ppg = int(page_no.name)
            else:
                ppg = request.env['website'].get_current_website().shop_ppg or 20

            ppr = request.env['website'].get_current_website().shop_ppr or 4

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")]
                             for v in attrib_list if v]
            attributes_ids = {v[0] for v in attrib_values}
            attrib_set = {v[1] for v in attrib_values}

            domain = self._get_search_domain(search, category, attrib_values)
            pricelist_context, pricelist = self._get_pricelist_context()
            request.context = dict(request.context, pricelist=pricelist.id,
                                   partner=request.env.user.partner_id)

            url = "/shop"
            if search:
                post["search"] = search
            if attrib_list:
                post['attrib'] = attrib_list
            if post:
                request.session.update(post)

            Product = request.env['product.template'].with_context(
                bin_size=True)
            session = request.session
            cate_for_price = None
            if category:
                url = "/shop/category/%s" % slug(category)
                cate_for_price = int(category)
            prevurl = request.httprequest.referrer
            if prevurl:
                if not re.search('/shop', prevurl, re.IGNORECASE):
                    request.session['pricerange'] = ""
                    request.session['min1'] = ""
                    request.session['max1'] = ""
                    request.session['curr_category'] = ""
            brand_list = request.httprequest.args.getlist('brand')
            brand_set = set([int(v) for v in brand_list])
            if brand_list:
                brandlistdomain = list(map(int, brand_list))
                domain += [('product_brand_id', 'in', brandlistdomain)]
                bran = []
                brand_obj = request.env['product.brands'].sudo().search(
                    [('id', 'in', brandlistdomain)])
                if brand_obj:
                    for vals in brand_obj:
                        if vals.name not in bran:
                            bran.append((vals.name, vals.id))
                    if bran:
                        request.session["brand_name"] = bran
            if not brand_list:
                request.session["brand_name"] = ''
            is_price_slider = request.website.viewref(
                'theme_scita.scita_price_slider_layout').active
            if is_price_slider:
                # For Price slider
                website_pricelist = request.website.get_current_pricelist()
                match_product = Product.search(domain)
                price_list = []
                if match_product:
                    for prod in match_product:
                        context = dict(request.env.context, quantity=1,
                                       pricelist=website_pricelist.id if website_pricelist else False)
                        prod_template = prod.with_context(context)

                        list_price = prod_template.price_compute('list_price')[prod_template.id]
                        price_tmp = prod_template.price if website_pricelist else list_price
                        if price_tmp:
                            price_list.append(price_tmp)
                if price_list:
                    product_slider_ids = [min(price_list), max(price_list)]
                    if product_slider_ids:
                        if post.get("range1") or post.get("range2") or not post.get("range1") or not post.get("range2"):
                            values['range1'] = math.floor(min(product_slider_ids))
                            values['range2'] = math.ceil(max(product_slider_ids))
                        if request.session.get('min1') or request.session.get('max1'):
                            price_product_list = []
                            if match_product:
                                for prod in match_product:
                                    context = dict(
                                        request.env.context, quantity=1, pricelist=website_pricelist.id if website_pricelist else False)
                                    prod_template = prod.with_context(context)

                                    list_price = prod_template.price_compute('list_price')[
                                        prod_template.id]
                                    price_tmp = prod_template.price if website_pricelist else list_price
                                    if price_tmp and price_tmp >= float(request.session['min1']) and price_tmp <= float(request.session['max1']):
                                        price_product_list.append(prod.id)
                            domain += [('id', 'in', price_product_list)]
                            request.session["pricerange"] = str(
                                request.session['min1']) + "-To-" + str(request.session['max1'])

                        if session.get('min1') and session['min1']:
                            values['min1'] = session["min1"]
                            values['max1'] = session["max1"]

            search_product = Product.search(domain, order=self._get_search_order(post))
            website_domain = request.website.website_domain()
            categs_domain = [('parent_id', '=', False)] + website_domain
            if search:
                search_categories = Category.search(
                    [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
                categs_domain.append(('id', 'in', search_categories.ids))
            else:
                search_categories = Category
            categs = Category.search(categs_domain)

            if cate_for_price:
                request.session['curr_category'] = float(cate_for_price)
            if request.session.get('default_paging_no'):
                ppg = int(request.session.get('default_paging_no'))
            keep = QueryURL('/shop', category=category and int(category),
                            search=search, attrib=attrib_list, order=post.get('order'))
            product_count = len(search_product)
            pager = request.website.pager(
                url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
            offset = pager['offset']
            products = search_product[offset: offset + ppg]

            ProductAttribute = request.env['product.attribute']
            if products:
                # get all products without limit
                attributes = ProductAttribute.search(
                    [('product_tmpl_ids', 'in', search_product.ids)])
            else:
                attributes = ProductAttribute.browse(attributes_ids)

            layout_mode = request.session.get('website_sale_shop_layout_mode')
            if not layout_mode:
                if request.website.viewref('website_sale.products_list_view').active:
                    layout_mode = 'list'
                else:
                    layout_mode = 'grid'
            values.update({
                'search': search,
                'category': category,
                'attrib_values': attrib_values,
                'attrib_set': attrib_set,
                'pager': pager,
                'pricelist': pricelist,
                'add_qty': add_qty,
                'products': products,
                'search_count': product_count,  # common for all searchbox
                'bins': TableCompute().process(products, ppg, ppr),
                'ppg': ppg,
                'ppr': ppr,
                'categories': categs,
                'attributes': attributes,
                'keep': keep,
                'search_categories_ids': search_categories.ids,
                'layout_mode': layout_mode,
                'brand_set': brand_set,
                'domain': domain,
            })
            if category:
                values['main_object'] = category
            return request.render("website_sale.products", values)
        else:
            return super(ScitaShop, self).shop(page=page, category=category, search=search, ppg=ppg, **post)

    @http.route(['''/allcategories''',
                 '''/allcategories/category/<model("product.public.category"):category>'''
                 ], type='http', auth="public", website=True)
    def shop_by_get_category(self, category=None, **post):
        cat = {}
        shop_category = None
        if category:
            if category.child_id:
                child = category.child_id
                cat.update({'pro': child})
        else:
            shop_category = child_cat_ids = request.env['product.public.category'].sudo().search(
                [('parent_id', '=', None)], order='name asc')
            cat.update({'pro': shop_category})
        return request.render("theme_scita.shop_by_category", cat)

    def get_brands_data(self, product_count, product_label):
        keep = QueryURL('/shop/get_it_brand', brand_id=[])
        value = {
            'website_brands': False,
            'brand_header': False,
            'keep': keep
        }
        if product_count:

            brand_data = request.env['product.brands'].sudo().search(
                [('active', '=', True)], limit=int(product_count))
            if brand_data:
                value['website_brands'] = brand_data
        if product_label:
            value['brand_header'] = product_label
        return value

    @http.route(['/shop/get_brand_slider'],
                type='json', auth='public', website=True)
    def get_brand_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['brand.snippet.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'website_brands': slider_header.collections_brands
            }
            return request.website.viewref(
                "theme_scita.retial_brand_snippet_1")._render(values)

    @http.route(['/shop/get_box_brand_slider'],
                type='json', auth='public', website=True)
    def get_box_brand_slider(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['brand.snippet.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'website_brands': slider_header.collections_brands
            }
            return request.website.viewref(
                "theme_scita.box_brand_snippet_4")._render(values)

    @http.route(['/shop/get_it_brand'],
                type='json', auth='public', website=True)
    def get_it_brand(self, **post):
        if post.get('slider-type'):
            slider_header = request.env['brand.snippet.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            values = {
                'slider_header': slider_header,
                'website_brands': slider_header.collections_brands
            }
            return request.website.viewref(
                "theme_scita.it_brand_snippet_1")._render(values)

    @http.route('/update_my_wishlist', type="http", auth="public", website=True)
    def qv_update_my_wishlist(self, **kw):
        if kw['prod_id']:
            self.add_to_wishlist(product_id=int(kw['prod_id']))
        return

    @http.route(['/product_category_img_slider'], type='json', auth='public', website=True)
    def config_cat_product(self, **post):
        context, pool = dict(request.context), request.env
        if post.get('slider-type'):
            slider_header = request.env['product.category.img.slider.config'].sudo().search(
                [('id', '=', int(post.get('slider-type')))])
            if not context.get('pricelist'):
                pricelist = request.website.get_current_pricelist()
                context = dict(request.context, pricelist=int(pricelist))
            else:
                pricelist = pool.get('product.pricelist').browse(
                    context['pricelist'])
        context.update({'pricelist': pricelist.id})
        from_currency = pool['res.users'].sudo().browse(
            SUPERUSER_ID).company_id.currency_id
        to_currency = pricelist.currency_id

        def compute_currency(price): return pool['res.currency']._convert(
            price, from_currency, to_currency, fields.Date.today())
        values = {
            'slider_header': slider_header,
            'slider_details': slider_header,
            'slider_header': slider_header,
            'compute_currency': compute_currency,
        }
        if slider_header.prod_cat_type == 'product':
            values.update({'slider_details': slider_header.collections_product})
        if slider_header.prod_cat_type == 'category':
            values.update({'slider_details': slider_header.collections_category})
        values.update({'slider_type': slider_header.prod_cat_type})
        return request.website.viewref("theme_scita.product_category_img_slider_config_view")._render(values)

    @http.route(['/theme_scita/product_category_slider'], type='json', auth="public", website=True)
    def get_product_category(self):
        slider_options = []
        option = request.env['product.category.img.slider.config'].sudo().search(
            [('active', '=', True)], order="name asc")
        for record in option:
            slider_options.append({'id': record.id,
                                   'name': record.name})
        return slider_options

    @http.route(['/theme_scita/get_current_wishlist'], type='json', auth="public", website=True)
    def get_current_wishlist(self):
        values = request.env['product.wishlist'].with_context(display_default_code=False).current()
        return request.env['ir.ui.view']._render_template("theme_scita.wishlist_products", dict(wishes=values))
    # Dynamic video banner url get start

    @http.route(['/video/video_url_get'],
                type='http', auth='public', website=True)
    def get_video_banner_url(self, **post):
        values = {
            "video_url": post.get('video_url')
        }
        return request.render(
            "theme_scita.sct_dynamic_banner_video_1", values)
    # Dynamic video banner url get End

    @http.route(['/shop/cart/update_custom'], type='json', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update_custom(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)
        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )
        return True

    @http.route(['/shop/cart/hover_update'], type='http', auth="public", website=True, sitemap=False)
    def cart_hover_update(self, **kw):
        order = request.website.sale_get_order()
        values = {
            'website_sale_order': order,
        }
        return request.render("theme_scita.hover_total", values, headers={'Cache-Control': 'no-cache'})

    @http.route("/shop/variant_change", auth="public", website=True, type='json', methods=['POST'])
    def on_variant_change(self, pro_id):
        product = request.env['product.product'].sudo().search(
            [('id', '=', int(pro_id))])
        values = {
            'is_default_code_disp': request.website.is_default_code,
            'default_code': product.default_code,
        }
        return values


class PWASupport(http.Controller):

    def get_asset_urls(self, asset_xml_id):
        qweb = request.env["ir.qweb"].sudo()
        assets = qweb._get_asset_nodes(asset_xml_id, {}, True, True)
        urls = []
        for asset in assets:
            if asset[0] == "link":
                urls.append(asset[1]["href"])
            if asset[0] == "script":
                urls.append(asset[1]["src"])
        return urls

    @http.route("/service_worker", type="http", auth="public")
    def service_worker(self):
        qweb = request.env["ir.qweb"].sudo()
        urls = []
        prefetch_urls = []
        urls.extend(self.get_asset_urls("web.assets_common"))
        urls.extend(self.get_asset_urls("web.assets_frontend"))
        version_list = []
        for url in urls:
            version_list.append(url.split("/")[3])
        cache_version = "-".join(version_list)
        mimetype = "text/javascript;charset=utf-8"
        prefetch_urls.append('/')
        prefetch_urls.append('/theme_scita/pwa/offline')
        prefetch_urls.append('/theme_scita/static/src/img/PWA/network-error.png')
        content = qweb._render(
            "theme_scita.pwa_service_worker",
            {"pwa_cache_version": cache_version, "urls_to_cache": prefetch_urls},
        )
        return request.make_response(content, [("Content-Type", mimetype)])

    @http.route("/theme_scita/manifest_file/<int:website_id>", type="http", auth="public")
    def pwa_manifest(self, website_id=None):
        qweb = request.env["ir.qweb"].sudo()
        website = request.env['website']
        current_website = website.search(
            [('id', '=', website_id)]) if website_id else request.website
        pwa_app_name = current_website.pwa_app_name or 'PWA App'
        pwa_app_short_name = current_website.pwa_app_short_name or 'PWA Application'
        image_72 = website.image_url(current_website, 'pwa_app_icon_512', '72x72')
        image_96 = website.image_url(current_website, 'pwa_app_icon_512', '96x96')
        image_128 = website.image_url(current_website, 'pwa_app_icon_512', '128x128')
        image_144 = website.image_url(current_website, 'pwa_app_icon_512', '144x144')
        image_152 = website.image_url(current_website, 'pwa_app_icon_512', '152x152')
        image_192 = website.image_url(current_website, 'pwa_app_icon_512', '192x192')
        image_256 = website.image_url(current_website, 'pwa_app_icon_512', '256x256')
        image_384 = website.image_url(current_website, 'pwa_app_icon_512', '384x384')
        image_512 = website.image_url(current_website, 'pwa_app_icon_512', '512x512')
        back_color = current_website.pwa_app_back_color or '#7C7BAD'
        theme_color = current_website.pwa_app_theme_color or '#ffffff'
        start_url = current_website.pwa_app_start_url or '/shop'
        mimetype = "application/json;charset=utf-8"
        content = qweb._render(
            "theme_scita.manifest_temp",
            {
                "pwa_name": pwa_app_name,
                "pwa_short_name": pwa_app_short_name,
                "image_72": image_72,
                "image_96": image_96,
                "image_128": image_128,
                "image_144": image_144,
                "image_152": image_152,
                "image_192": image_192,
                "image_256": image_256,
                "image_384": image_384,
                "image_512": image_512,
                "start_url": start_url,
                "background_color": back_color,
                "theme_color": theme_color,
            },
        )
        return request.make_response(content, [("Content-Type", mimetype)])

    @http.route("/theme_scita/pwa/offline", type="http", auth="public", website=True)
    def pwa_offline_page(self):
        values = {}
        return request.render("theme_scita.pwa_offline_template", values)

    @http.route("/theme_scita/shop/quick_view", type="json", auth="public", website=True)
    def scita_quick_view_data(self,product_id=None):
        product = request.env['product.template'].browse(int(product_id))
        return request.env['ir.ui.view']._render_template("theme_scita.shop_quick_view_modal", {'product':product})
        
    @http.route("/theme_scita/shop/cart_view", type="json", auth="public", website=True)
    def scita_cart_view_data(self,product_id=None):
        product = request.env['product.template'].browse(int(product_id))
        return request.env['ir.ui.view']._render_template("theme_scita.shop_cart_view_modal", {'product':product})

