# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from datetime import datetime, timedelta


class TestDev(models.Model):
    _name = 'test_dev.test_dev'
    _description = 'Basic model for test dev'

    name = fields.Char()
    birth_date = fields.Date('Birth Date')
    age = fields.Integer(compute='_compute_age', store=True, readonly=True)
    description = fields.Text(' Write any Description')

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
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    # sale_order_ids = fields.One2many('sale.order', 'partner_id', string='Sale orders',
    #                                  help='Sale orders related to this customer')
    purchase_count = fields.Integer(string="Purchase Count (This Month)", compute="_compute_purchase_count")
    is_eligible = fields.Boolean(string="Eligible for Prize/Discount", compute="_compute_eligibility", store=True)
    discount_percentage = fields.Float(string="Discount(%)", default=0.0,
                                       help='discount percentage is applied if the customer is eligible for a prize.')
    date_checked = fields.Date(string="Date Checked", default=fields.Date.today)
    prize_description = fields.Html(string='Prize Description')

    # @api.depends('sale_order_ids.date_order', 'sale_order_ids.state')
    # def _compute_purchase_count(self):
    #     """
    #        Compute the total purchase count and set the discount if eligible.
    #        """
    #     for record in self:
    #         # Filter for confirmed or done sale orders
    #         confirmed_orders = record.sale_order_ids.filtered(
    #             lambda so: so.state in ['sale', 'done'] and so.date_order.month == date.today().month
    #         )
    #         # Count the number of items purchased in the current month
    #         record.purchase_count = len(confirmed_orders)
    #         # Apply discount if eligible (e.g., purchase count >= 3)
    #         record.discount_percentage = 10.0 if record.purchase_count >= 3 else 0.0
    #
    # @api.depends('sale_order_ids')
    # def _compute_eligibility(self):
    #     for record in self:
    #         # Dictionary to track product purchases by month and year
    #         purchases_by_month = {}
    #
    #         for so in record.sale_order_ids.filtered(lambda so: so.state in ['sale', 'done']):
    #             order_month = so.date_order.month
    #             order_year = so.date_order.year
    #
    #             for line in so.order_line:
    #                 product_id = line.product_id.id
    #
    #                 # Build a unique key for product and month/year
    #                 key = (product_id, order_month, order_year)
    #                 if key not in purchases_by_month:
    #                     purchases_by_month[key] = 0
    #
    #                 purchases_by_month[key] += 1
    #
    #         # Check eligibility based on purchases in the same month
    #         eligible = any(count >= 3 for count in purchases_by_month.values())
    #
    #         # Apply discount or prize logic
    #         if eligible:
    #             record.discount_percentage = 10.0  # Example prize logic
    #         else:
    #             record.discount_percentage = 0.0

    @api.depends('customer_id', 'product_id')
    def _compute_purchase_count(self):
        for record in self:
            if record.customer_id and record.product_id:
                print("*************", record.customer_id)
                # Calculate start and end of the current month
                today = fields.Date.today()
                start_of_month = today.replace(day=1)
                end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

                # Search for purchases in sale.order.line within the current month
                purchase_count = self.env['sale.order.line'].search_count([
                    ('order_id.partner_id', '=', record.customer_id.id),
                    ('product_id', '=', record.product_id.id),
                    ('order_id.date_order', '>=', start_of_month),
                    ('order_id.date_order', '<=', end_of_month)
                ])

                record.purchase_count = purchase_count
                # check if the product is purchased 3 or more times in the month
                record.is_eligible = purchase_count >= 3  # Eligible if 3 or more purchases
            else:
                record.purchase_count = 0
                record.is_eligible = False

    def apply_discount_or_prize(self):
        """Logic to apply discount or prizes directly to sale orders."""
        for record in self:
            if record.is_eligible:
                record.discount_percentage = 10.0
            else:
                record.discount_percentage = 0.0
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
