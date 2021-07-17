# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

import pytz
import time

from operator import itemgetter
from itertools import groupby

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from _datetime import date
from odoo.exceptions import Warning


class StockValuationCategory(models.AbstractModel):
    _name = 'report.stock_valuation_on_date.stock_valuation_ondate_report'
    _description = 'stock_valuation_ondate_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise Warning(_("Form content is missing, this report cannot be printed."))
        return {
            'doc_ids': self._ids,
            'docs': self,
            'data': data,
            'time': time,
            'get_warehouse_name': self.get_warehouse_name,
            'get_warehouses_block': self._get_warehouses_block,
            'get_company': self._get_company,
            'get_product_name': self._product_name,
            'get_categ': self._get_categ,
            'get_lines': self._get_lines,
            'get_cost': self._get_cost,
            'get_subtotal_cost': self._get_subtotal_cost
            }

    def _get_warehouses_block(self, warehouse_ids, company_id):
        warehouse_obj = self.env['stock.warehouse']
        warehouses = 'ALL'
        if warehouse_ids:
            warehouse_rec = warehouse_obj.search([
                                  ('id', 'in', warehouse_ids),
                                  ('company_id', '=', company_id)
                                  ])
            if warehouse_rec:
                warehouses = ",".join([x.name for x in warehouse_rec])
            else:
                warehouses = '-'
        return warehouses

    def _get_company(self, company_ids):
        res_company_pool = self.env['res.company']
        if not company_ids:
            company_ids = res_company_pool.search([]).ids

        # filter to only have warehouses.
        selected_companies = []
        for company_id in company_ids:
            if self.env['stock.warehouse'].search([('company_id', '=', company_id)]):
                selected_companies.append(company_id)

        return res_company_pool.browse(selected_companies).read(['name', 'currency_id'])

    def get_warehouse_name(self, warehouse_ids):
        """
        Return warehouse names
            - WH A, WH B...
        """
        warehouse_obj = self.env['stock.warehouse']
        if not warehouse_ids:
            warehouse_ids = [x.id for x in warehouse_obj.search([])]
        war_detail = warehouse_obj.read(warehouse_ids, ['name'])
        return ', '.join([lt['name'] or '' for lt in war_detail])

    def _get_cost(self, company_id, product_id, inventory_date, ending_inventory):
        """
        Return:
            - inventory cost on  date
            - Working only for average and standard cost
            - Need to check deeply if you want to get a values on date
        """
        #inventory_date = self.convert_withtimezone(inventory_date + ' 00:00:00')
#         if isinstance(inventory_date, date):
#             inventory_date = inventory_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         inventory_date = datetime.strptime(inventory_date, DEFAULT_SERVER_DATE_FORMAT)
#         inventory_date = fields.Datetime.to_string(
#                    inventory_date.replace(hour=23, minute=59, second=59))
#         if ending_inventory == 0.0:
#             return 0.0
# 
        to_check = self.env['product.product'].browse(product_id)
#         stock_value = to_check.with_context(to_date=inventory_date, force_company=company_id).value_svl
        #return round(float(stock_value) / float(ending_inventory), 2)
        return to_check.with_company(company_id).standard_price

    def _get_subtotal_cost(self, cost, ending_inv, current_record):
        subtotal_cost = cost and ending_inv and round((cost * ending_inv), 2) or 0.0
        current_record.update({'subtotal_cost': subtotal_cost})
        return subtotal_cost

    def _begin_qty(self, product_id, begin_dict):
        """
            Get Begining Qty
        """
        bqty_value = product_id and begin_dict and list(filter(lambda x: x['product_id'] == product_id, begin_dict))
        return bqty_value and bqty_value[0].get('begining_qty', 0.0) or 0.0

    def _ending_qty(self, values_dict, begining_qty):
        """
            Get Ending Qty
        """
        product_qty_in = values_dict.get('product_qty_in', 0.0) or 0.0
        product_qty_out = values_dict.get('product_qty_out', 0.0) or 0.0
        product_qty_adjustment = values_dict.get('product_qty_adjustment', 0.0) or 0.0
        return begining_qty + product_qty_in + product_qty_out + product_qty_adjustment

    # Report totally depends on picking type, need to check in deeply when directly move created from anywhere.
    def category_wise_value(self, start_date, end_date, locations, filter_product_categ_ids=[]):
        """
        Complete data with category wise
            - In Qty (Inward Quantity to given location)
            - Out Qty(Outward Quantity to given location)
            - Adjustment Qty(Inventory Loss movements to given location: out/in both: out must be - ,In must be + )
        Return:
            [{},{},{}...]
        """

        self._cr.execute('''
                        SELECT pp.id AS product_id, pt.categ_id,
                            0.0 AS begining_qty,
                            sum((
                                CASE WHEN sourcel.usage = 'internal' AND smline.location_id in %s  AND destl.usage !='inventory' 
                                THEN -(smline.qty_done)
                                ELSE 0.0 
                                END
                            )) AS product_qty_out,
                            sum((
                                CASE WHEN destl.usage = 'internal' AND smline.location_dest_id in %s AND sourcel.usage !='inventory'
                                THEN (smline.qty_done)
                                ELSE 0.0 
                                END
                            )) AS product_qty_in,
                            sum((
                                CASE WHEN sourcel.usage = 'inventory' AND smline.location_dest_id in %s 
                                THEN  (smline.qty_done)
                                WHEN destl.usage ='inventory' AND smline.location_id in %s 
                                THEN -(smline.qty_done)
                                ELSE 0.0 
                                END
                            )) AS product_qty_adjustment
                        
                        FROM product_product pp
                            LEFT JOIN stock_move_line smline ON (smline.product_id = pp.id AND smline.location_id != smline.location_dest_id AND smline.state = 'done' AND smline.date >= %s and smline.date <= %s)
                            LEFT JOIN stock_location sourcel ON (smline.location_id=sourcel.id)
                            LEFT JOIN stock_location destl ON (smline.location_dest_id=destl.id)
                            LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                        GROUP BY pt.categ_id, pp.id order by pt.categ_id
                        ''',(tuple(locations),tuple(locations),tuple(locations),tuple(locations),start_date, end_date))


        values = self._cr.dictfetchall()

        self._cr.execute(''' 
                            SELECT product_id, coalesce(sum(begining_qty), 0.0) AS begining_qty
                            FROM
                                ((
                                SELECT
                                    smline.product_id as product_id,
                                    coalesce(sum(-smline.qty_done)::decimal, 0.0) as begining_qty
                                FROM stock_move_line smline 
                                WHERE smline.date <  %s AND (smline.location_id in %s) 
                                AND smline.state='done'
                                GROUP BY  smline.product_id
                                ) 
                                UNION ALL
                                (
                                SELECT
                                    smline.product_id as id,
                                    coalesce(sum(smline.qty_done)::decimal, 0.0) as begining_qty
                                FROM stock_move_line smline 
                                WHERE smline.date <  %s AND (smline.location_dest_id in %s) 
                                AND smline.state='done'
                                GROUP BY  smline.product_id
                                ))
                                AS foo
                            GROUP BY product_id
                            ''',(start_date, tuple(locations), start_date, tuple(locations)))

        beginings = self._cr.dictfetchall()

        for none_to_update in values:
            product_id = none_to_update and none_to_update.get('product_id') or False
            begining_qty = self._begin_qty(product_id, beginings)
            none_to_update.update({'begining_qty': begining_qty})
            if not none_to_update.get('product_qty_out'):
                none_to_update.update({'product_qty_out':0.0})
            if not none_to_update.get('product_qty_in'):
                none_to_update.update({'product_qty_in':0.0})
            ending_qty = self._ending_qty(none_to_update, begining_qty)
            none_to_update.update({'ending_qty': ending_qty})

        # filter by categories
        if filter_product_categ_ids:
            values = self._remove_product_cate_ids(values, filter_product_categ_ids)
        return values

    def _remove_zero_inventory(self, values):
        final_values = []
        for rm_zero in values:
            if rm_zero['product_qty_in'] == 0.0 and rm_zero['product_qty_out'] == 0.0 and rm_zero['product_qty_adjustment'] == 0.0:
                pass
            else: final_values.append(rm_zero)
        return final_values

    def _remove_product_cate_ids(self, values, filter_product_categ_ids):
        final_values = []
        for rm_products in values:
            if rm_products['categ_id'] not in filter_product_categ_ids:
                pass
            else: final_values.append(rm_products)
        return final_values

    def _get_categ(self, categ):
        """
        Find category name with id
        """
        return self.env['product.category'].browse(categ).read(['name'])[0]['name']

    def _product_name(self, product_id):
        """
        Find product name and assign to it
        """
        product = self.env['product.product'].browse(product_id).name_get()
        return product and product[0] and product[0][1] or ''

    def find_warehouses(self, company_id):
        """
        Find all warehouses
        """
        return [x.id for x in self.env['stock.warehouse'].search([('company_id', '=', company_id)])]

    def _find_locations(self, warehouses):
        """
            Find all warehouses stock locations and its childs.
        """
        warehouse_obj = self.env['stock.warehouse']
        location_obj = self.env['stock.location']
        stock_ids = []
        for warehouse in warehouses:
            stock_ids.append(warehouse_obj.sudo().browse(warehouse).view_location_id.id)
        # stock_ids = [x['view_location_id'] and x['view_location_id'][0] for x in warehouse_obj.sudo().read(self.cr, 1, warehouses, ['view_location_id'])]
        return [l.id for l in location_obj.search([('location_id', 'child_of', stock_ids)])]

    def convert_withtimezone(self, userdate):
        """ 
            Convert to Time-Zone with compare to UTC
        """
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATETIME_FORMAT)
        tz_name = self.env.context.get('tz') or self.env.user.tz
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            # not need if you give default datetime into entry ;)
            user_datetime = user_date  # + relativedelta(hours=24.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_lines(self, data, company):
        """
        Process:
            Pass start date, end date, locations to get data from moves,
            Merge those data with locations,
        Return:
            {category : [{},{},{}...], category : [{},{},{}...],...}
        """

        start_date = self.convert_withtimezone(data['form']['start_date'] + ' 00:00:00')
        end_date = self.convert_withtimezone(data['form']['end_date'] + ' 23:59:59')

        warehouse_ids = data['form'] and data['form'].get('warehouse_ids', []) or []
        filter_product_categ_ids = data['form'] and data['form'].get('filter_product_categ_ids') or []
        if not warehouse_ids:
            warehouse_ids = self.find_warehouses(company)

        # find all locations from all warehouse for that company
        location_id = data['form'] and data['form'].get('location_id') or False
        if location_id:
            locations = [location_id]
        else:
            locations = self._find_locations(warehouse_ids)

        # get data from all warehouses.
        records = self.category_wise_value(start_date, end_date, locations, filter_product_categ_ids)

        # records by categories
        sort_by_categories = sorted(records, key=itemgetter('categ_id'))
        records_by_categories = dict((k, [v for v in itr]) for k, itr in groupby(sort_by_categories, itemgetter('categ_id')))

        return records_by_categories
