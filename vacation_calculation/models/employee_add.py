from odoo import api, fields, models


class EmployeeAdd(models.Model):
    _inherit = 'hr.employee'

    day_price = fields.Float(string='Day Price', readonly=True)

    @api.onchange('contract_id.wage', 'contract_id.working_days')
    def _compute_day_price(self):
        for record in self:
            if record.contract_id.wage and record.contract_id.working_days:
                record.day_price = record.contract_id.wage / record.contract_id.working_days
