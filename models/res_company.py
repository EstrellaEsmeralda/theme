# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_desc = fields.Text(string="Company Description", translate=True)
    header_link_name_1 = fields.Char(
        string='URL 1 Name', help='Header Sidebar Link 1 Name', default="Blog", translate=True)
    header_link_1 = fields.Char(string='URL 1 Hyperlink',
                                help='Header Sidebar Link 1 Hyperlink', default="/blog")
    header_link_name_2 = fields.Char(
        string='URL 2 Name', help='Header Sidebar Link 2 Name', default="Contact Us", translate=True)
    header_link_2 = fields.Char(string='URL 2 Hyperlink',
                                help='Header Sidebar Link 2 Hyperlink', default="/contactus")
    header_link_name_3 = fields.Char(
        string='URL 3 Name', help='Header Sidebar Link 3 Name', default="About Us", translate=True)
    header_link_3 = fields.Char(string='URL 3 Hyperlink',
                                help='Header Sidebar Link 3 Hyperlink', default="/aboutus")
    # Delivery location configuration
    delivery_icon = fields.Char(string='Icon', help='Delivery Icon', default="fa fa-map-marker")
    delivery_text = fields.Char(string='Title', help='Delivery Text',
                                default="Delivery", translate=True)
    delivery_btn_name = fields.Char(
        string='Button Name', help='Delivery Button Name', default="Check", translate=True)
    delivery_blank_msg = fields.Char(string='Blank Validation Message',
                                     help='Delivery zip code is blank', default="Please enter the zip code", translate=True)
    delivery_success_msg = fields.Char(
        string='Success Message', help='Delivery zip code is available message', default="Available", translate=True)
    delivery_fail_msg = fields.Char(
        string='Fail Message', help='Delivery zip code is not available message', default="Currently not available", translate=True)
