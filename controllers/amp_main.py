from werkzeug.exceptions import Forbidden, NotFound
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website.controllers.main import QueryURL
import json


class CustomAMP(WebsiteSale):

    @http.route(['/shop/product/amp/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    def custom_amp_view(self, product, category='', search='', **post):
        if request.website.is_amp_enable:
            ProductCategory = request.env['product.public.category']
            if category:
                category = ProductCategory.browse(int(category)).exists()
            categs = ProductCategory.search([('parent_id', '=', False)])
            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
            attrib_set = {v[1] for v in attrib_values}

            keep = QueryURL('/shop/amp', category=category and category.id,
                            search=search, attrib=attrib_list)
            values = {
                'main_object': product,
                'product': product,
                'category': category,
                'categories': categs,
                'keep': keep,
            }

            return request.render("theme_scita.apm_product_view", values)
        else:
            raise NotFound()

    @http.route([
        '''/shop/amp''',
        '''/shop/amp/page/<int:page>''',
        '''/shop/amp/category/<model("product.public.category"):category>''',
        '''/shop/amp/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=False)
    def shop_amp(self, page=0, category=None, search='', ppg=False, **post):
        if request.website.is_amp_enable:
            add_qty = int(post.get('add_qty', 1))
            Category = request.env['product.public.category']
            if category:
                category = Category.search([('id', '=', int(category))], limit=1)
                if not category or not category.can_access_from_current_website():
                    raise NotFound()
            else:
                category = Category

            page_no = request.env['product.per.page.no'].sudo().search(
                [('set_default_check', '=', True)])
            if page_no:
                ppg = int(page_no.name)
            else:
                ppg = result.qcontext['ppg']

            ppr = request.env['website'].get_current_website().shop_ppr or 4

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
            attributes_ids = {v[0] for v in attrib_values}
            attrib_set = {v[1] for v in attrib_values}

            domain = self._get_search_domain(search, category, attrib_values)
            if request.session.get('default_paging_no'):
                ppg = int(request.session.get('default_paging_no'))
            keep = QueryURL('/shop/amp', category=category and int(category),
                            search=search, attrib=attrib_list, order=post.get('order'))

            pricelist_context, pricelist = WebsiteSale._get_pricelist_context(self)

            request.context = dict(request.context, pricelist=pricelist.id,
                                   partner=request.env.user.partner_id)

            url = "/shop/amp"
            if search:
                post["search"] = search
            if attrib_list:
                post['attrib'] = attrib_list

            Product = request.env['product.template'].with_context(bin_size=True)

            search_product = Product.search(domain)
            website_domain = request.website.website_domain()
            categs_domain = [('parent_id', '=', False)] + website_domain
            if search:
                search_categories = Category.search(
                    [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
                categs_domain.append(('id', 'in', search_categories.ids))
            else:
                search_categories = Category
            categs = Category.search(categs_domain)

            if category:
                url = "/shop/amp/category/%s" % slug(category)

            product_count = len(search_product)
            pager = request.website.pager(url=url, total=product_count,
                                          page=page, step=ppg, scope=7, url_args=post)
            products = Product.search(
                domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

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

            values = {
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
            }
            if category:
                values['main_object'] = category
            return request.render("theme_scita.apm_shop_page_view", values)
        else:
            raise NotFound()
