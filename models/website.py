# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.
import math
import werkzeug
import base64
import os
import re
import uuid
from lxml import etree
from odoo import models, api, fields
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

PPG = 18


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    is_megamenu = fields.Boolean(string='Is megamenu...?')
    megamenu_view_type = fields.Selection([('cat_megamenu', 'Category Megamenu'),
                                           ('cat_img_megamenu',
                                            "Category Image Megamenu"),
                                           ('prod_megamenu', "Products Megamenu"),
                                           ('pages_megamenu', "Pages Megamenu"),
                                           ('service_page_megamenu',
                                            "Service Menu"),
                                           ('service_content_megamenu',
                                            "Service Content Menu"),
                                           ('service_banner_megamenu',
                                            "Service Banner Menu")
                                           ],
                                          default='cat_megamenu',
                                          string="Megamenu View Type")
    is_service_menu = fields.Boolean(
        string='Is service menu...?', default=False)
    is_service_content_menu = fields.Boolean(
        string='Is service content menu...?', default=False)
    megamenu_size = fields.Selection([('medium', 'Medium'),
                                      ('large', 'Large')],
                                     default='medium',
                                     string="Megamenu Size")

    megamenu_type = fields.Selection([
        ('2_col', '2 Columns'),
        ('3_col', '3 Columns'),
        ('4_col', '4 Columns')],
        default='3_col',
        string="Megamenu type")
    megamenu_type1 = fields.Selection([('1_col', '1 Columns'),
                                       ('2_col', '2 Columns'),
                                       ('3_col', '3 Columns'),
                                       ('4_col', '4 Columns')],
                                      default='3_col',
                                      string="Megamenu columns")
    category_slider = fields.Boolean(
        string='Want to display category slider', default=False)
    carousel_header_name = fields.Char(string="Slider label",
                                       default="Latest",
                                       translate=True,
                                       help="Header name for carousel slider in megamenu")
    category_slider_position = fields.Selection([('left', 'Left'), ('right', 'Right')],
                                                default='left', string="Category Slider Position")

    display_menu_footer = fields.Boolean(string="Display menu footer", default=False,
                                         help="For displaying footer in megamenu")
    menu_footer = fields.Text(string="Footer content",
                              translate=True,
                              help="Footer name for megamenu")
    megamenu_product_ids = fields.Many2many("product.template", string="Products", domain=[
        ('website_published', '=', True)])

    is_img_banner = fields.Boolean(
        string='Want to display Banner', default=False)
    img_banner = fields.Binary(
        string="image banner", help="Menu image banner for your menu")
    img_banner_position = fields.Selection(
        [('left', 'Left'), ('right', 'Right')], default='left', string="Image Banner Position")
    img_menu = fields.Binary(
        string="Menu image", help="Menu image  your menu")
    menu_desc = fields.Text(string="Menu description",
                            translate=True,
                            help="Menu description")
    service_content = fields.Text(string="Menu Content",
                                  translate=True,
                                  help="sub menu")
    banner_content = fields.Text(string="banner Content",
                                 translate=True,
                                 help="Banner description")

    @api.onchange('parent_id')
    def _on_change_parent(self):
        """ Password parent
        """
        if self.parent_id.megamenu_view_type == 'service_page_megamenu' or self.parent_id.megamenu_view_type == 'service_content_megamenu':
            self.is_service_menu = True
        else:
            self.is_service_menu = False


class website(models.Model):
    _inherit = 'website'

    header_logo = fields.Binary('Header Logo')
    footer_logo = fields.Binary('Footer Logo')
    # For Multi image
    no_extra_options = fields.Boolean(string='Want to customize multi-image slider',
                                      default=False,
                                      help="Slider with all options for next, previous, play, pause, fullscreen, hide/show thumbnail panel.")
    interval_play = fields.Char(string='slideshow interval', default='5000',
                                help='With this field you can set the interval play time between two images.')
    enable_disable_text = fields.Boolean(string='Enable text panel',
                                         default=True,
                                         help='Enable/Disable text which is visible on the image in multi image.')
    color_opt_thumbnail = fields.Selection([
        ('default', 'Default'),
        ('b_n_w', 'B/W'),
        ('sepia', 'Sepia'),
        ('blur', 'Blur'), ],
        default='default',
        string="Thumbnail overlay effects")
    thumbnail_panel_position = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right'),
        ('bottom', 'Bottom'),
    ], default='left',
        string='Thumbnails panel position',
        help="Select the position where you want to display the thumbnail panel in multi image.")
    change_thumbnail_size = fields.Boolean(
        string="Change thumbnail size", default=False)
    thumb_height = fields.Char(string='Thumb height', default=86)
    thumb_width = fields.Char(string='Thumb width', default=66)
    # For Brand setting
    is_brand_display = fields.Boolean(
        string="Brand display in product page", default=False)
    brand_display_option = fields.Selection([
        ('name', 'Name'),
        ('logo', 'Logo'),
    ], default='logo',
        string='Brand Display Option',
        help="Select the option for brand logo  or name display.")
    is_default_code = fields.Boolean(
        string="Default code display in product page", default=False)
    # For social setting
    is_social_display = fields.Boolean(
        string="Social share is display in product page", default=False)
    is_amp_enable = fields.Boolean(
        string="Enable AMP", default=True)

    # Product per grid
    product_display_grid = fields.Selection([('2', '2 Grid'), ('3', '3 Grid'), ('4', '4 Grid'), ('list', 'List View')],
                                            default='3', string='View Default Option', help="Display default selection in website shop page product grid.")

    @api.model
    def theme_scita_payment_icons(self):
        """ This function returns the list of payment icons
        which are supported by payment acquirers that are published
        """
        return self.env['payment.icon'].sudo().search([
            ('acquirer_ids.state', 'in', ['enabled', 'test'])], limit=5)

    # for product brand
    def get_product_brands(self, category, **post):
        domain = []
        if category:
            cat_id = []
            if category != None:
                for ids in category:
                    cat_id.append(ids.id)
                domain += ['|', ('public_categ_ids.id', 'in', cat_id),
                           ('public_categ_ids.parent_id', 'in', cat_id)]
        else:
            domain = []
        product_ids = self.env["product.template"].sudo(
        ).search(domain)
        domain_brand = [
            ('product_ids', 'in', product_ids.ids or []), ('product_ids', '!=', False)]
        brands = self.env['product.brands'].sudo().search(domain_brand)
        return brands

    # for hr.employee
    def get_snippet_employee(self):
        employee = self.env['hr.employee'].sudo().search(
            [('include_inourteam', '=', 'True')])
        return employee

    def get_snippet_blog_post(self):
        post = self.env['blog.post'].sudo().search(
            [('website_published', '=', 'True')])
        return post

    # For pages megamenu
    def get_megamenu_pages(self, submenu):
        menus = self.env['website.menu'].sudo().search(
            [('parent_id', '=', submenu.id)])
        return menus

    # For pages megamenu count
    def get_megamenu_pages_count(self, submenu):
        page_menu_count = self.env['website.menu'].sudo().search_count(
            [('parent_id', '=', submenu.id)])
        return page_menu_count

    # For category megamenu
    def get_public_product_category(self, submenu):
        categories = self.env['product.public.category'].search([('parent_id', '=', False), ("website_id", "in", (False, request.website.id)),
                                                                 ('include_in_megamenu',
                                                                  '!=', False),
                                                                 ('menu_id', '=', submenu.id)],
                                                                order="name")
        return categories
    # For category megamenu

    def get_all_public_product_category(self, submenu):
        categories = self.env['product.public.category'].search([("website_id", "in", (False, request.website.id)),
                                                                 ('include_in_megamenu',
                                                                  '!=', False),
                                                                 ('menu_id', '=', submenu.id)],
                                                                order="name")
        return categories

    # For child category megamenu
    def get_public_product_child_category(self, children):
        child_categories = []
        for child in children:
            categories = self.env['product.public.category'].search([
                ('id', '=', child.id),
                ("website_id", "in", (False, request.website.id)),
                ('include_in_megamenu', '!=', False)], order="name")
            if categories:
                child_categories.append(categories)
        return child_categories

    # For Sorting products
    def get_sort_by_data(self):
        request.session['product_sort_name'] = ''
        sort_by = self.env['biztech.product.sortby'].search([])
        return sort_by

    # For setting current sort list
    def set_current_sorting_data(self):
        sort_name = request.session.get('product_sort_name')
        return sort_name

    # For first last pager
    def get_pager_selection(self):
        prod_per_page = self.env['product.per.page'].search([])
        prod_per_page_no = self.env['product.per.page.no'].search([])
        values = {
            'name': prod_per_page.name,
            'page_no': prod_per_page_no,
        }
        return values

    def get_current_pager_selection(self):
        page_no = request.env['product.per.page.no'].sudo().search(
            [('set_default_check', '=', True)])
        if request.session.get('default_paging_no'):
            return int(request.session.get('default_paging_no'))
        elif page_no:
            return int(page_no.name)
        else:
            return PPG

    def get_parent_category_breadcum(self, category):
        data = []
        parent_cat = False
        if category:
            cat_data = self.env['product.public.category'].search(
                [('id', '=', int(category))])
            data.append(cat_data)
            parent_cat = cat_data
            if cat_data and cat_data.parent_id:
                parent_cat = cat_data.parent_id
                data.append(parent_cat)
                while parent_cat.parent_id:
                    parent_cat = parent_cat.parent_id
                    data.append(parent_cat)
            data.reverse()
        return data

    # For multi image
    def get_multiple_images(self, product_id=None):
        productsss = False
        if product_id:
            products = self.env['scita.product.images'].search(
                [('biz_product_tmpl_id', '=', product_id)], order='sequence')
            if products:
                return products
        return productsss

    @api.model
    def pager(self, url, total, page=1, step=30, scope=5, url_args=None):
        res = super(website, self). pager(url=url,
                                          total=total,
                                          page=page,
                                          step=step,
                                          scope=scope,
                                          url_args=url_args)
        # Compute Pager
        page_count = int(math.ceil(float(total) / step))

        page = max(1, min(int(page if str(page).isdigit() else 1), page_count))
        scope -= 1

        pmin = max(page - int(math.floor(scope/2)), 1)
        pmax = min(pmin + scope, page_count)

        if pmax - pmin < scope:
            pmin = pmax - scope if pmax - scope > 0 else 1

        def get_url(page):
            _url = "%s/page/%s" % (url, page) if page > 1 else url
            if url_args:
                if url_args.get('tag'):
                    del url_args['tag']
                if url_args.get('range1'):
                    del url_args['range1']
                if url_args.get('range2'):
                    del url_args['range2']
                if url_args.get('max1'):
                    del url_args['max1']
                if url_args.get('min1'):
                    del url_args['min1']
                if url_args.get('sort_id'):
                    del url_args['sort_id']
                if not url_args.get('tag') and not url_args.get('range1') and not url_args.get('range2') and not url_args.get('max1') and not url_args.get('min1') and not url_args.get('sort_id'):
                    _url = "%s?%s" % (_url, werkzeug.url_encode(url_args))
            return _url
        res.update({
            # Overrite existing
            "page_start": {
                'url': get_url(pmin),
                'num': pmin
            },
            "page_previous": {
                'url': get_url(max(pmin, page - 1)),
                'num': max(pmin, page - 1)
            },
            "page_next": {
                'url': get_url(min(pmax, page + 1)),
                'num': min(pmax, page + 1)
            },
            "page_end": {
                'url': get_url(pmax),
                'num': pmax
            },
            'page_first': {
                'url': get_url(1),
                'num': 1
            },
            'page_last': {
                'url': get_url(int(res['page_count'])),
                'num': int(res['page_count'])
            },
            'pages': [
                {'url': get_url(page), 'num': page}
                for page in range(pmin, pmax+1)
            ]
        })
        return res
        
    def get_categories(self, category=None):
        cat = {}
        shop_category = request.env['product.public.category'].sudo().search(
            [('parent_id', '=', None)], order='name asc')
        cat.update({'categ': shop_category})
        return cat