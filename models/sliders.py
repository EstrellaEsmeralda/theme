# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BlogSlider(models.Model):
    _name = 'blog.slider.config'
    _description = 'Blog Slider'

    name = fields.Char(string="Slider name", default='Blogs',
                       help="""Slider title to be displayed on 
                       website like Our Blogs, Latest Blog Post and etc...""",
                       required=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    sub_title = fields.Text(string="Slider sub title", default='Lorem ipsum is simply dummy text of the printing and typesetting industry.',
                            help="""Slider sub title to be display""", translate=True)
    no_of_counts = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], string="Counts",
                                    default='3',
                                    help="No of blogs to be displayed in slider.",
                                    required=True)
    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='''Sliding speed of a slider can be set 
                                   from here and it will be in milliseconds.''')
    collections_blog_post = fields.Many2many('blog.post', 'blogpost_slider_rel', 'slider_id',
                                             'post_id',
                                             string="Collections of blog posts", required=True, domain="[('is_published', '=', True)]")


class CategorySlider(models.Model):
    _name = 'category.slider.config'
    _description = 'Categories Slider'

    name = fields.Char(string="Slider name", required=True,
                       translate=True,
                       help="""Slider title to be displayed on website
                        like Best Categories, Latest and etc...""")
    active = fields.Boolean(string="Active", default=True)

    collections_category = fields.Many2many('product.public.category',
                                            'theme_scita_category_slider_rel',
                                            'slider_id', 'cat_id',
                                            string="Collections of category")


class MultiSlider(models.Model):
    _name = 'multi.slider.config'
    _description = "Configuration of Multi slider"

    name = fields.Char(string="Slider name", default='Trending',
                       required=True, translate=True,
                       help="Slider title to be displayed on website like Best products, Latest and etc...")
    active = fields.Boolean(string="Active", default=True)

    auto_rotate = fields.Boolean(string='Auto Rotate Slider', default=True)
    sliding_speed = fields.Integer(string="Slider sliding speed", default='5000',
                                   help='Sliding speed of a slider can be set from here and it will be in milliseconds.')
    is_rating_enable = fields.Boolean(
        string='Show Product Rating', default=True)
    no_of_collection = fields.Selection([('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                        string="No. of collections to show", default='2',
                                        required=True,
                                        help="No of collections to be displayed on slider.")

    label_collection_1 = fields.Char(string="1st collection name", default='First collection',
                                     required=True, translate=True,
                                     help="Collection label to be displayed in website like Men, Women, Kids, etc...")
    collection_1_ids = fields.Many2many('product.template', 'product_slider_collection_1_rel', 'slider_id',
                                        'prod_id',
                                        required=True,
                                        string="1st product collection", domain="[('is_published', '=', True)]")

    label_collection_2 = fields.Char(string="2nd collection name", default='Second collection',
                                     required=True, translate=True,
                                     help="Collection label to be displayed in website like Men, Women, Kids, etc...")
    collection_2_ids = fields.Many2many('product.template', 'product_slider_collection_2_rel', 'slider_id',
                                        'prod_id',
                                        required=True,
                                        string="2nd product collection", domain="[('is_published', '=', True)]")

    label_collection_3 = fields.Char(string="3rd collection name", default='Third collection', translate=True,
                                     # required=True,
                                     help="Collection label to be displayed in website like Men, Women, Kids, etc...")
    collection_3_ids = fields.Many2many('product.template', 'product_slider_collection_3_rel', 'slider_id',
                                        'prod_id',
                                        # required=True,
                                        string="3rd product collection", domain="[('is_published', '=', True)]")

    label_collection_4 = fields.Char(string="4th collection name", default='Fourth collection', translate=True,
                                     # required=True,
                                     help="Collection label to be displayed in website like Men, Women, Kids, etc...")
    collection_4_ids = fields.Many2many('product.template', 'product_slider_collection_4_rel', 'slider_id',
                                        'prod_id',
                                        # required=True,
                                        string="4th product collection", domain="[('is_published', '=', True)]")

    label_collection_5 = fields.Char(string="5th collection name", default='Fifth collection', translate=True,
                                     # required=True,
                                     help="Collection label to be displayed in website like Men, Women, Kids, etc...")
    collection_5_ids = fields.Many2many('product.template', 'product_slider_collection_5_rel', 'slider_id',
                                        'prod_id',
                                        # required=True,
                                        string="5th product collection", domain="[('is_published', '=', True)]")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    include_inourteam = fields.Boolean(
        string="Enable to make the employee visible in snippet")
    emp_social_twitter = fields.Char(
        string="Twitter account", default="https://twitter.com/Odoo")
    emp_social_facebook = fields.Char(
        string="Facebook account", default="https://www.facebook.com/Odoo")
    emp_social_linkdin = fields.Char(
        string="Linkedin account", default="https://www.linkedin.com/company/odoo")
    emp_description = fields.Text(
        string="Short description about employee", translate=True)


class BrandSnippetConfiguration(models.Model):
    _name = 'brand.snippet.config'
    _description = " Brand Snippet Configuration"

    name = fields.Char(string="Name", default='Trending brand', required=True, translate=True,
                       help="Title to be displayed on website like Latest and etc...")
    active = fields.Boolean(string="Active", default=True, required=True)
    collections_brands = fields.Many2many('product.brands', 'product_brands_slider_rel',
                                          'brand_id', 'slider_id', string="Collections of Brand", required=True)


class ProductCategorySlider(models.Model):
    _name = 'product.category.img.slider.config'
    _description = 'product category image Slider'

    name = fields.Char(string="Slider name", default='Trend',
                       help="""Slider title to be displayed""",
                       required=True, translate=True)
    img_banner = fields.Binary(string="Image banner",
                               help="""Image banner""")
    img_link = fields.Char(string="Image Url", default='#',
                           help="""Image Url""")
    links = fields.Text(string="Links",
                        help="""Image banner""")
    active = fields.Boolean(string="Active", default=True)
    no_of_column = fields.Selection([('3', '3'), ('4', '4'), ('5', '5')], string="No of column",
                                    default='3',
                                    help="No of product display in slider.")
    prod_cat_type = fields.Selection([('product', 'Product'), ('category', 'Category')],
                                     string="Type of slider", default='product', required=True,
                                     help="Select product or category for whom you want to show a slider.")
    collections_product = fields.Many2many('product.template', 'scita_product_slider_rel', 'slider_id',
                                           'prod_id', string="Collections of product")
    collections_category = fields.Many2many('product.public.category', 'scita_category_slider_rel',
                                            'slider_id', 'cat_id', string="Collections of category")


class ProductSnippetConfiguration(models.Model):
    _name = 'product.snippet.configuration'
    _description = "Add Multiple Product In Snippet"

    name = fields.Char(string='Name', default="Trending", required=True)
    sub_title = fields.Char(string="Sub Title", default="Lorem Ipsum is simply dummy text.",)
    active = fields.Boolean(
        string="Active", default=True)
    collection_of_products = fields.Many2many('product.template', 'product_configuration_rel', 'slider_id',
                                              'prod_id',
                                              required=True,
                                              string="Collection Of Products", domain="[('is_published', '=', True)]")
