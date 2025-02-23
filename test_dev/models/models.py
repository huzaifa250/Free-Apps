# -*- coding: utf-8 -*-
import calendar

from odoo import models, fields, api
from datetime import date
from datetime import datetime, timedelta


class TestDev(models.Model):
    _name = 'test_dev.test_dev'
    _description = 'Basic model for test dev'

    name = fields.Char(string='Name')
    active = fields.Boolean(default=True, string='Active')
    birth_date = fields.Date('Birth Date')
    age = fields.Integer(compute='_compute_age', store=True, readonly=True)
    description = fields.Text('Write any Description')

    @api.depends('birth_date')
    def _compute_age(self):
        """calculate the age of the person
        according to birth year
        """
        for rec in self:
            if rec.birth_date:
                # Calculate age as the difference in years
                rec.age = date.today().year - rec.birth_date.year
            else:
                rec.age = 0


# -If the customer bought item 3 or more for the same product, apply the prize or discount percentage.

class CustomerPurchaseTracker(models.Model):
    _name = 'custom.purchase.tracker'
    _description = 'Customer Purchase Tracker'
    _inherit = 'mail.thread'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', required=True)
    product_id = fields.Many2one(comodel_name='product.product', string="Product", required=True)
    purchase_count = fields.Integer(string="Purchase Count (This Month)", compute="_compute_purchase_count")
    is_eligible = fields.Boolean(string="Eligible for Prize/Discount", compute="_compute_eligibility", store=True)
    discount_percentage = fields.Float(string="Discount(%)", default=0.0, tracking=True,
                                       help='discount percentage is applied if the customer is eligible for a prize.')
    date_checked = fields.Date(string="Date Checked", default=fields.Date.today)
    prize_description = fields.Html(string='Prize Description')

    @api.depends('customer_id', 'product_id')
    def _compute_purchase_count(self):
        for record in self:
            if not record.customer_id or not record.product_id:
                record.purchase_count = 0
                record.is_eligible = False
                return
                # print("*************", record.customer_id)
            # Calculate start and end of the current month
            today = fields.Date.today()
            start_of_month = today.replace(day=1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            end_of_month = today.replace(day=last_day)
            # end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            # Search for purchases in sale.order.line within the current month
            purchase_count = self.env['sale.order.line'].search_count([
                ('order_id.partner_id', '=', record.customer_id.id),
                ('product_id', '=', record.product_id.id),
                ('order_id.date_order', '>=', start_of_month),
                ('order_id.date_order', '<=', end_of_month),
                ('order_id.state', 'in', ['sale', 'done'])
            ])

            record.purchase_count = purchase_count
            # check if the product is purchased 3 or more times in the month
            record.is_eligible = purchase_count >= 3

    def apply_discount_or_prize(self):
        """Logic to apply discount or prizes directly to sale orders."""
        for record in self:
            if not record.is_eligible:
                return False
            record.discount_percentage = 10.0

            # Search for eligible sale orders in the current month
            today = fields.Date.today()
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            sale_lines = self.env['sale.order.line'].search([
                ('order_id.partner_id', '=', record.customer_id.id),
                ('product_id', '=', record.product_id.id),
                ('order_id.date_order', '>=', start_of_month),
                ('order_id.date_order', '<=', end_of_month)
            ])

            for line in sale_lines:
                if line.order_id.state in ['sale', 'done']:
                    line.discount = record.discount_percentage
