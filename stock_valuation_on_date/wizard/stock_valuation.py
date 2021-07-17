# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)
import xlwt
from io import BytesIO
import base64
from . import xls_format

from odoo import models, api, fields, _
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from ..report.stock_valuation import StockValuationCategory


class StockValuationDateReport(models.TransientModel,
                               StockValuationCategory):
    _name = 'stock.valuation.ondate.report'
    _description = 'stock.valuation.ondate.report'

    company_id = fields.Many2one('res.company', string='Company')
    warehouse_ids = fields.Many2many('stock.warehouse', string='warehouse')
    location_id = fields.Many2one('stock.location', string='Location')
    start_date = fields.Date(
         string='From Date',
         required=True,
         default=fields.Date.context_today
         )
    end_date = fields.Date(
         string='To Date',
         required=True,
         default=fields.Date.context_today
         )
#     inventory_date = fields.Date(
#          string='To Date',
#          required=True,
#          default=lambda *a: (parser.parse(datetime.now().strftime(DF)))
#          )
    filter_product_ids = fields.Many2many('product.product', string='Products')
    filter_product_categ_ids = fields.Many2many(
        'product.category',
        string='Categories'
        )
    only_summary = fields.Boolean(
      string='Display Only Summary?',
      help="True, it will display only total summary of categories.",
      )

    @api.onchange('company_id')
    def onchange_company_id(self):
        """
        Make warehouse compatible with company
        """
        warehouse_ids = self.env['stock.warehouse'].sudo().search([])
        if self.company_id:
            warehouse_ids = self.env['stock.warehouse'].sudo().search([('company_id', '=', self.company_id.id)])
        return {
                'domain':
                        {
                         'warehouse_ids': [('id', 'in', [x.id for x in warehouse_ids])]
                         },
                'value':
                        {
                         'warehouse_ids': False
                        }
                }

    @api.onchange('warehouse_ids', 'company_id')
    def onchange_warehouse(self):
        """
        Make warehouse compatible with company
        """
        location_obj = self.env['stock.location']
        location_ids = location_obj.search([('usage', '=', 'internal')])
        total_warehouses = self.warehouse_ids
        if total_warehouses:
            addtional_ids = []
            for warehouse in total_warehouses:
                store_location_id = warehouse.view_location_id.id
                addtional_ids.extend([y.id for y in location_obj.search([('location_id', 'child_of', store_location_id), ('usage', '=', 'internal')])])
            location_ids = addtional_ids
        elif self.company_id:
            total_warehouses = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)])
            addtional_ids = []
            for warehouse in total_warehouses:
                store_location_id = warehouse.view_location_id.id
                addtional_ids.extend([y.id for y in location_obj.search([('location_id', 'child_of', store_location_id), ('usage', '=', 'internal')])])
            location_ids = addtional_ids
        else:
            location_ids = [p.id for p in location_ids]
        return {
                  'domain':
                            {
                             'location_id': [('id', 'in', location_ids)]
                             },
                  'value':
                        {
                            'location_id': False
                        }
                }

    def print_report(self):
        """
            Print report either by warehouse or product-category
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        datas = {
                 'form':
                    {
                        'company_id': self.company_id and [self.company_id.id] or [],
                        'warehouse_ids': [y.id for y in self.warehouse_ids],
                        'location_id': self.location_id and self.location_id.id or False,
                        #'inventory_date': self.inventory_date,
                        'start_date': self.start_date.strftime(DF),
                        'end_date': self.end_date.strftime(DF),
                        'only_summary': self.only_summary,
                        'id': self.id,
                        'filter_product_ids': [p.id for p in self.filter_product_ids],
                        'filter_product_categ_ids': [p.id for p in self.filter_product_categ_ids] 
                    }
                }

        if [y.id for y in self.warehouse_ids] and (not self.company_id):
            self.warehouse_ids = []
            raise Warning(_('Please select company of those warehouses to get correct view.\nYou should remove all warehouses first from selection field.'))
        #return self.env['report'].with_context(landscape=True).get_action(self, 'stock_valuation_on_date.stock_valuation_ondate_report', data=datas)
        return self.env.ref(
                            'stock_valuation_on_date.action_stock_valuation_ondate'
                            ).with_context(landscape=True).report_action(self, data=datas)

    def _to_company(self, company_ids):
        company_obj = self.env['res.company']
        warehouse_obj = self.env['stock.warehouse']
        if not company_ids:
            company_ids = [x.id for x in company_obj.search([])]

        # filter to only have warehouses.
        selected_companies = []
        for company_id in company_ids:
            if warehouse_obj.search([('company_id', '=', company_id)]):
                selected_companies.append(company_id)

        return selected_companies

    def xls_get_warehouses(self, warehouses, company_id):
        warehouse_obj = self.env['stock.warehouse']
        if not warehouses:
            return 'ALL'

        warehouse_rec = warehouse_obj.search([
                                              ('id', 'in', warehouses),
                                              ('company_id', '=', company_id),
                                              ])
        return warehouse_rec \
            and ",".join([x.name for x in warehouse_rec]) or '-'

    @api.model
    def _product_detail(self, product_id):
        product = self.env['product.product'].browse(product_id)
        variant = ", ".join([v.name for v in product.product_template_attribute_value_ids])
        product_name = variant and "%s (%s)" % (
                                    product.name, variant) or product.name
        return product_name, product.barcode, product.default_code

    @api.model
    def _value_existed(
                      self,
                      beginning_inventory,
                      product_qty_in,
                      product_qty_out,
                      product_qty_adjustment,
                      ending_inventory
                      ):
        value_existed = False
        if beginning_inventory or product_qty_in or product_qty_out or product_qty_adjustment or \
                ending_inventory:
            value_existed = True
        return value_existed

    def print_xls_report(self):
        """
            Print ledger report
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        workbook = xlwt.Workbook()

        M_header_tstyle = xls_format.font_style(position='center', bold=1, border=1, fontos='black', font_height=400, color='grey')
        header_tstyle_c = xls_format.font_style(position='center', bold=1, border=1, fontos='black', font_height=180, color='grey')
        other_tstyle_c = xls_format.font_style(position='center', fontos='black', font_height=180, color='grey')
        other_tstyle_cr = xls_format.font_style(position='center', fontos='purple_ega', bold=1, font_height=180, color='grey')
        other_tstyle_r = xls_format.font_style(position='right', fontos='purple_ega', bold=1, font_height=180, color='grey')
        other_tstyle_grandc = xls_format.font_style(position='center', fontos='purple_ega', bold=1,border=1, font_height=180, color='grey')
        other_tstyle_grandr = xls_format.font_style(position='right', fontos='purple_ega', bold=1,border=1, font_height=180, color='grey')

        datas = {
                 'form':
                    {
                        'company_id': self.company_id and [self.company_id.id] or [],
                        'warehouse_ids': [y.id for y in self.warehouse_ids],
                        'location_id': self.location_id and self.location_id.id or False,
                        #'inventory_date': self.inventory_date,
                        'start_date': self.start_date.strftime(DF),
                        'end_date': self.end_date.strftime(DF),
                        'only_summary': self.only_summary,
                        'id': self.id,
                        'filter_product_ids': [p.id for p in self.filter_product_ids],
                        'filter_product_categ_ids': [p.id for p in self.filter_product_categ_ids] 
                    }
                }
        company_ids = self._to_company(
                       self.company_id and [self.company_id.id] or [])

        company_obj = self.env['res.company']
        summary = self.only_summary and 'Summary Report' or 'Detail Report'
        for company in company_ids:
            c_rec = company_obj.sudo().browse(company)
            Hedaer_Text = '%s' % (str(c_rec.name))
            sheet = workbook.add_sheet(Hedaer_Text)
            sheet.set_panes_frozen(True)
            sheet.set_horz_split_pos(9)
            sheet.row(0).height = 256 * 3
            sheet.write_merge(0, 0, 0, 11, Hedaer_Text, M_header_tstyle)

            total_lines = self._get_lines(datas, company)
            warehouses = self.xls_get_warehouses(
                         [y.id for y in self.warehouse_ids], company)
            sheet_start_header = 3
            sheet_start_value = 4
            sheet.write_merge(sheet_start_header, sheet_start_header, 0, 1, 'Date', header_tstyle_c)
            sheet.write_merge(sheet_start_value, sheet_start_value, 0, 1, self.start_date.strftime(DF) + ' To ' + self.end_date.strftime(DF), other_tstyle_cr)
            sheet.write_merge(sheet_start_header, sheet_start_header, 2, 3, 'Company', header_tstyle_c)
            sheet.write_merge(sheet_start_value, sheet_start_value, 2, 3, c_rec.name, other_tstyle_c)
            sheet.write_merge(sheet_start_header, sheet_start_header, 4, 5, 'Warehouse(s)', header_tstyle_c)
            sheet.write_merge(sheet_start_value, sheet_start_value, 4, 5, warehouses, other_tstyle_c)
            sheet.write_merge(sheet_start_header, sheet_start_header, 6, 7, 'Currency', header_tstyle_c)
            sheet.write_merge(sheet_start_value, sheet_start_value, 6, 7, c_rec.currency_id.name, other_tstyle_c)
            sheet.write_merge(sheet_start_header, sheet_start_header, 8, 9, 'Display', header_tstyle_c)
            sheet.write_merge(sheet_start_value, sheet_start_value, 8, 9, summary, other_tstyle_c)

            if self.only_summary:
                header_row_start = 8
                sheet.col(0).width = 256 * 25
                sheet.write(header_row_start, 0, 'Category Name ', header_tstyle_c)
                sheet.col(1).width = 256 * 25
                sheet.write(header_row_start, 1, 'Total Beginning', header_tstyle_c)
                sheet.col(2).width = 256 * 25
                sheet.write(header_row_start, 2, 'Total Received', header_tstyle_c)
                sheet.col(3).width = 256 * 25
                sheet.write(header_row_start, 3, 'Total Sales', header_tstyle_c)
                sheet.col(4).width = 256 * 25
                sheet.write(header_row_start, 4, 'Total Adjustment', header_tstyle_c)
                sheet.col(5).width = 256 * 25
                sheet.write(header_row_start, 5, 'Total Ending', header_tstyle_c)
                sheet.col(6).width = 256 * 25
                sheet.write(header_row_start, 6, 'Total Values', header_tstyle_c)
                row = 9
                grand_total_qty_in, grand_total_qty_out,\
                    grand_total_product_qty_adjustment, \
                    grand_total_beginning_inventory,\
                    grand_total_ending_inventory, grand_total_subtotal_cost = 0.0, \
                    0.0, 0.0, 0.0, 0.0, 0.0
                for key, values in total_lines.items():
                    total_qty_in, total_qty_out, \
                        total_product_qty_adjustment, \
                        total_beginning_inventory,\
                        total_ending_inventory, total_subtotal_cost = 0.0, \
                        0.0, 0.0, 0.0, 0.0, 0.0
                    for line in values:
                        product_qty_in = line.get('product_qty_in', 0.0) or 0.0
                        product_qty_out = line.get('product_qty_out', 0.0) or 0.0
                        product_qty_adjustment = line.get('product_qty_adjustment', 0.0) or 0.0
                        beginning_inventory = line.get('begining_qty', 0.0) or 0.0
                        ending_inventory = line.get('ending_qty', 0.0) or 0.0
#                         beginning_inventory = self._get_beginning_inventory(
#                                       datas,
#                                       company,
#                                       line.get('product_id', '') or '',
#                                       line
#                                       )
#                         ending_inventory = self._get_ending_inventory(
#                           product_qty_in,
#                           product_qty_out,
#                           product_qty_adjustment,
#                           )
                        unit_cost = self._get_cost(
                          company,
                          line.get('product_id', '') or '',
                          self.end_date,
                          ending_inventory
                          )
                        subtotal_cost = self._get_subtotal_cost(
                          unit_cost,
                          ending_inventory,
                          line
                          )
                        total_beginning_inventory += beginning_inventory
                        total_qty_in += product_qty_in
                        total_qty_out += product_qty_out
                        total_product_qty_adjustment += product_qty_adjustment
                        total_ending_inventory += ending_inventory
                        total_subtotal_cost += subtotal_cost

                    grand_total_beginning_inventory += total_beginning_inventory
                    grand_total_qty_in += total_qty_in
                    grand_total_qty_out += total_qty_out
                    grand_total_product_qty_adjustment += total_product_qty_adjustment
                    grand_total_ending_inventory += total_ending_inventory
                    grand_total_subtotal_cost += total_subtotal_cost
                    sheet.write(
                            row,
                            0,
                            self._get_categ(key),
                            other_tstyle_c)
                    sheet.write(
                            row,
                            1,
                            "%.2f" % total_beginning_inventory,
                            other_tstyle_r)
                    sheet.write(
                            row,
                            2,
                            "%.2f" % total_qty_in,
                            other_tstyle_r)
                    sheet.write(
                            row,
                            3,
                            "%.2f" % total_qty_out,
                            other_tstyle_r)
                    sheet.write(
                            row,
                            4,
                            "%.2f" % total_product_qty_adjustment,
                            other_tstyle_r)
                    sheet.write(
                            row,
                            5,
                            "%.2f" % total_ending_inventory,
                            other_tstyle_r)
                    sheet.write(
                            row,
                            6,
                            "%.2f" % total_subtotal_cost,
                            other_tstyle_r)
                    row += 1

                sheet.write(
                        row,
                        0,
                        "Grand Total",
                        other_tstyle_grandc)
                sheet.write(
                        row,
                        1,
                        "%.2f" % grand_total_beginning_inventory,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        2,
                        "%.2f" % grand_total_qty_in,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        3,
                        "%.2f" % grand_total_qty_out,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        4,
                        "%.2f" % grand_total_product_qty_adjustment,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        5,
                        "%.2f" % grand_total_ending_inventory,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        6,
                        "%.2f" % grand_total_subtotal_cost,
                        other_tstyle_grandr)
            else:
                header_row_start = 8
                sheet.write(header_row_start, 0, 'Category Name ', header_tstyle_c)
                sheet.col(0).width = 256 * 20
                sheet.write(header_row_start, 1, 'Product Name ', header_tstyle_c)
                sheet.col(1).width = 256 * 40
                sheet.write(header_row_start, 2, 'Product Barcode ', header_tstyle_c)
                sheet.col(2).width = 256 * 20
                sheet.write(header_row_start, 3, 'Default Code ', header_tstyle_c)
                sheet.col(3).width = 256 * 20
                sheet.write(header_row_start, 4, 'Beginning', header_tstyle_c)
                sheet.col(4).width = 256 * 20
                sheet.write(header_row_start, 5, 'Received', header_tstyle_c)
                sheet.col(5).width = 256 * 20
                sheet.write(header_row_start, 6, 'Sales', header_tstyle_c)
                sheet.col(7).width = 256 * 20
                sheet.write(header_row_start, 7, 'Adjustments', header_tstyle_c)
                sheet.col(8).width = 256 * 20
                sheet.write(header_row_start, 8, 'Ending', header_tstyle_c)
                sheet.col(9).width = 256 * 20
                sheet.write(header_row_start, 9, 'Cost', header_tstyle_c)
                sheet.col(10).width = 256 * 20
                sheet.write(header_row_start, 10, 'Total Value', header_tstyle_c)
                sheet.col(11).width = 256 * 20
                row = 9
                grand_total_qty_in, grand_total_qty_out, \
                    grand_total_product_qty_adjustment, \
                    grand_total_beginning_inventory,\
                    grand_total_ending_inventory, grand_total_subtotal_cost = 0.0, \
                    0.0, 0.0, 0.0, 0.0, 0.0
                for values in total_lines.values():
                    for line in values:
                        product_qty_in = line.get('product_qty_in', 0.0) or 0.0
                        product_qty_out = line.get('product_qty_out', 0.0) or 0.0
                        product_qty_adjustment = line.get('product_qty_adjustment', 0.0) or 0.0
                        beginning_inventory = line.get('begining_qty', 0.0) or 0.0
                        ending_inventory = line.get('ending_qty', 0.0) or 0.0
#                         beginning_inventory = self._get_beginning_inventory(
#                                       datas,
#                                       company,
#                                       line.get('product_id', '') or '',
#                                       line
#                                       )
#                         ending_inventory = self._get_ending_inventory(
#                           product_qty_in,
#                           product_qty_out,
#                           product_qty_adjustment,
#                           )
                        unit_cost = self._get_cost(
                          company,
                          line.get('product_id', '') or '',
                          self.end_date,
                          ending_inventory
                          )
                        subtotal_cost = self._get_subtotal_cost(
                          unit_cost,
                          ending_inventory,
                          line
                          )
                        product_name, product_barcode, product_code = \
                            self._product_detail(line.get('product_id', '') or '')
                        grand_total_beginning_inventory += beginning_inventory
                        grand_total_qty_in += product_qty_in
                        grand_total_qty_out += product_qty_out
                        grand_total_product_qty_adjustment += product_qty_adjustment
                        grand_total_ending_inventory += ending_inventory
                        grand_total_subtotal_cost += subtotal_cost
                        if self._value_existed(
                                          beginning_inventory,
                                          product_qty_in,
                                          product_qty_out,
                                          product_qty_adjustment,
                                          ending_inventory
                                          ):
                            sheet.write(
                                    row,
                                    0,
                                    self._get_categ(line.get('categ_id', '') or ''),
                                    other_tstyle_c)
                            sheet.write(
                                    row,
                                    1,
                                    product_name or '',
                                    other_tstyle_c)
                            sheet.write(
                                    row,
                                    2,
                                    product_barcode or '',
                                    other_tstyle_c)
                            sheet.write(
                                    row,
                                    3,
                                    product_code or '',
                                    other_tstyle_c)
                            sheet.write(
                                    row,
                                    4,
                                    "%.2f" % beginning_inventory,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    5,
                                    "%.2f" % product_qty_in,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    6,
                                    "%.2f" % product_qty_out,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    7,
                                    "%.2f" % product_qty_adjustment,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    8,
                                    "%.2f" % ending_inventory,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    9,
                                    "%.2f" % unit_cost,
                                    other_tstyle_r)
                            sheet.write(
                                    row,
                                    10,
                                    "%.2f" % subtotal_cost,
                                    other_tstyle_r)
                            row += 1

                sheet.write(
                        row,
                        3,
                        "Grand Total",
                        other_tstyle_grandc)
                sheet.write(
                        row,
                        4,
                        "%.2f" % grand_total_beginning_inventory,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        5,
                        "%.2f" % grand_total_qty_in,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        6,
                        "%.2f" % grand_total_qty_out,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        7,
                        "%.2f" % grand_total_product_qty_adjustment,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        8,
                        "%.2f" % grand_total_ending_inventory,
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        9,
                        "-",
                        other_tstyle_grandr)
                sheet.write(
                        row,
                        10,
                        "%.2f" % grand_total_subtotal_cost,
                        other_tstyle_grandr)

        stream = BytesIO()
        workbook.save(stream)

        export_obj = self.env['stock.valuation.success.box']
        res_id = export_obj.create({
                'file': base64.encodestring(stream.getvalue()),
                'fname': "Stock Valuation Report.xls"
                })
        return {
             'type': 'ir.actions.act_url',
             'url': '/web/binary/download_document?model=stock.valuation.success.box&field=file&id=%s&filename=Stock Valuation Report.xls'%(res_id.id),
             'target': 'new',
             }


class StockValuationSuccessBox(models.TransientModel):
    _name = 'stock.valuation.success.box'
    _description = 'stock.valuation.success.box'

    file = fields.Binary('File', readonly=True)
    fname = fields.Char('Text')
