# -*- coding: utf-8 -*-
import base64
import time

from odoo import api, fields, models, SUPERUSER_ID, tools
from pytz import timezone, UTC
from odoo.tools.translate import _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_round


class CalculateVacation(models.Model):
    _name = 'calculate.vacation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    """
   Calculate the amount of vacation: When a time off request is approved,
   use the start date, end date, and the number of working days to calculate the amount of vacation. 
   amount can be stored in the time off request model and linked to the corresponding account using the "account_id"
    """

    # def _get_employee_id(self):
    #     employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    #     return employee_rec.id
    ####################################################################################################
    # @api.depends('contract_id.wage', 'employee_id')
    # # @api.onchange('employee_id')
    # def _compute_day_price(self):
    #     for record in self:
    #         if record.employee_id and record.contract_id.wage:
    #             print('Cheeeeeeeeeeeeeeeeeck', record.employee_id, record.contract_id.wage)
    #             record.day_price = record.contract_id.wage / 30

    ################################################################################################################

    # @api.depends('start_date', 'end_date', 'day_price')
    # def _compute_total_amount(self):
    """
    compute total amount as number of taken days * day price 
    so if he/she sold more than one day the computed total will gonna be equal no_of_days
       """
    #     for request in self:
    #         if request.start_date and request.end_date and request.day_price:
    #             delta = request.end_date - request.start_date # this will give u number of days from the range dates
    #             request.total_amount = delta.days * request.day_price

    # @api.depends('wage', 'leave_balance')
    # def compute_leave_amount(self):
    #     # ?????????????
    #     for lev in self:
    #         # print("++++++++++++++++++++")
    #         lev.leave_amount = 0.0
    #         if lev.leave_balance > 0:
    #             result = lev.wage / 30 * lev.leave_balance
    #             lev.leave_amount = result

    # total = salary + leave_amount + other_allowances - other_deduction
    # @api.depends('working_days', 'other_allowances', 'leave_amount')
    # def compute_total(self):
    #     for too in self:
    #         if too.notice_month:
    #             tt = too.wage
    #             too.total_receivables = tt
    #         else:
    #             salary = too.wage / 30 * too.working_days
    #             total = salary + too.leave_amount + too.other_allowances - too.other_deduction
    #             too.total_receivables = total
    selection = [('draft', 'To Submit'), ('cancel', 'Cancelled'), ('confirm', 'To Approve'),
                 ('hr_officer', 'HR Officer'),
                 ('hr_manager', 'HR Manager'),
                 ('finance_officer', 'Finance Officer'),
                 ('finance_manager', 'Finance Manager'),
                 ('co_approve', 'CO approved'), ('validate1', 'Second Approval'),
                 ('validate', 'Approved')]
    state = fields.Selection(selection, copy=False, tracking=True, string='Status', default='draft')

    employee_id = fields.Many2one('hr.employee', readonly=False,
                                  required=True, string='Employee')
    user_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user, string='User')
    dept_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id', string='Department')
    day_date = fields.Datetime(default=fields.Datetime.now, string='Today', required=False)
    end_date = fields.Date('End Date')
    # total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount')
    sell_days = fields.Integer(string='Sell days', required=True, )
    amount = fields.Float(string='Amount', required=False)
    # day_price = fields.Float(compute='_compute_day_price', string='Day price', readonly=True, store=True)
    price = fields.Float('Day price')
    rest = fields.Float(compute='_calc_leave', required=False, readonly=True, store=True, string='Rest',
                        help='The remaining from actual balance')

    currency_id = fields.Many2one('res.currency', string='Currency')
    # working_days = fields.Float(related='contract_id.working_days', store=True)
    leave_type_id = fields.Many2one('hr.leave.type',
                                    string='Leave Type', copy=False,
                                    track_visibility='onchange')
    remaining_leaves = fields.Float(related='leave_type_id.remaining_leaves', required=False,
                                    string='Remaining Leaves')
    holiday_status_id = fields.Many2one(
        'hr.leave.type', string='Time Off Type', required=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, )

    debit_id = fields.Many2one('account.account', string='Debit account')
    credit_id = fields.Many2one('account.account', string='Credit account')
    journal_name = fields.Many2one(comodel_name="account.journal", string="Journal")
    account_id = fields.Many2one(comodel_name="account.move", string="Account", required=False, readonly=False)
    leave_id = fields.Many2one('hr.leave.allocation', string='Leave Type', copy=False, track_visibility='onchange')

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        """
        find an active contract for the selected employee.
        calculate the wage per day based on that contract's wage
        :return:
        """

        if self.employee_id:
            contract = self.env['hr.contract'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', 'open')
            ], limit=1)
            wage_per_day = contract.wage / 30 if contract else 0.0
            self.price = wage_per_day
        else:
            self.price = 0.0

# another way but it's not perfect
#     @api.onchange('employee_id')
#     def onchange_employee_id(self):
#         if self.employee_id:
#             contract = self.employee_id.contract_ids.filtered(lambda c: c.state == 'open')
#             wage_per_day = contract.wage / 30 if contract else 0.0
#             self.price = wage_per_day
#         else:
#             self.price = 0.0

    def action_draft(self):
        self.state = 'draft'

    def button_cancel(self):
        self.leave_id.unlink()
        self.state = 'cancel'

    def action_hr_officer(self):
        return self.write({'state': 'hr_officer'})

    def action_hr_manager(self):
        return self.write({'state': 'hr_manager'})

    def action_finance_officer(self):
        self.write({'state': 'finance_officer'})

    def action_finance_manager(self):
        for rec in self:
            create_leave = self.env['hr.leave.allocation'].create({
                'employee_id': 1,
                'name': 'sold Leave',
                'holiday_status_id': self.leave_type_id.id,
                'allocation_type': 'regular',
                'number_of_days': - int(rec.sell_days)
            })
            create_leave.action_approve()
            create_leave.action_validate()
            vals = {
                'journal_id': rec.journal_name.id,
                'ref': rec.employee_id.name,
                'state': 'draft', }
            move = self.env['account.move'].create(vals)
            print("*****************", move.name)
            rec.account_id = move.id
            rec.write({'state': 'finance_manager'})

    @api.constrains('sell_days')
    def check_sell_days(self):
        for rec in self:
            if rec.sell_days <= 0:
                raise ValidationError(_('The sell days Must be Greater Than 0..!'))

    def action_co_approve(self):
        # if self.holiday_status_id.co_id:
        #     self.activity_schedule('vacation.mail_act_vacation_approval',
        #                            note=f'Vacation approval requested {self.name}',
        #                            user_id=self.holiday_status_id.co_id.id)
        return self.write({'state': 'co_approve'})

    def action_validate1(self):
        self.write({'state': 'validate1'})

    def action_validate(self):
        for holiday in self:
            if holiday.state not in ['confirm', 'validate1']:
                raise UserError(_('Allocation request must be confirmed in order to approve it.'))
            holiday.write({'state': 'validate'})

    def action_confirm(self):
        for rec in self:
            if rec.remaining_leaves <= 0:
                raise ValidationError(_('The Remaining Leaves days Must be Greater Than 0..!'))
                # print("############################", rec.remaining_leaves)
            else:
                rec.write({
                    'state': 'confirm'
                })

    @api.depends('sell_days', 'remaining_leaves')
    def _calc_leave(self):
        """
        if u sell days the remaining leave will decrease by the amount sell

        :return:
        """
        for rec in self:
            if int(rec.sell_days == 0):
                print("_________^_^__________________")
            else:
                no = int(rec.sell_days)
                rec.rest = rec.remaining_leaves - no


class InheritLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    _sql_constraints = [
        ('type_value',
         "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or "
         "(holiday_type='category' AND category_id IS NOT NULL) or "
         "(holiday_type='department' AND department_id IS NOT NULL) or "
         "(holiday_type='company' AND mode_company_id IS NOT NULL))",
         "The employee, department, company or employee category of this request is missing. Please make sure that your user login is linked to an employee."),
        ('duration_check', "CHECK ( number_of_days <= 0 )", "The number of days must be greater than 00."),
        ('number_per_interval_check', "CHECK(number_per_interval > 0)",
         "The number per interval should be greater than 0"),
        ('interval_number_check', "CHECK(interval_number > 0)", "The interval number should be greater than 0"),
    ]
