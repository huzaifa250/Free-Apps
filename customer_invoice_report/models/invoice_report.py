from odoo import models, fields, api


class InvoiceReport(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'معالج تقرير الفواتير'

    start_date = fields.Date(string='تاريخ البداية', required=True, default='2024-06-01')
    end_date = fields.Date(string='تاريخ النهاية', required=True, default='2024-07-31')
    partner_ids = fields.Many2many('res.partner', string='الزبائن', required=True)

    # pass enter data from wiz to report
    def generate_report(self):
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'partner_ids': self.partner_ids.ids,
        }
        return self.env.ref('customer_invoice_report.action_invoice_report').report_action(self, data=data)


class InvoiceReportAb(models.AbstractModel):
    _name = 'report.customer_invoice_report.invoice_report_template'
    _description = 'تقرير الفواتير المخصص'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Extract filter parameters from the data dictionary
        start_date = data['start_date']
        end_date = data['end_date']
        partner_ids = data['partner_ids']

        # Fetch customer invoices
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),  # Customer invoices only
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
            ('partner_id', 'in', partner_ids),
            ('state', '!=', 'draft'),
        ])

        # Fetch sale orders
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date),
            ('partner_id', 'in', partner_ids),
            ('state', 'in', ['sale', 'done']),  # Confirmed or completed orders
        ])

        # Combine data(so and invoices) into a single list
        # combined_data = []
        # Add invoices to the list
        # for inv in invoices:
        #     combined_data.append({
        #         'type': 'Invoice',
        #         'number': inv.name,
        #         'date': inv.invoice_date,
        #         'customer': inv.partner_id.name,
        #         'amount': inv.amount_total,
        #     })

        # Add sale orders to the list
        # for so in sale_orders:
        #     combined_data.append({
        #         'type': 'Sale Order', # indicate invoice or so
        #         'number': so.name,
        #         'date': so.date_order,
        #         'customer': so.partner_id.name,
        #         'amount': so.amount_total,
        #     })

        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': invoices,
            # 'combined_data': combined_data,
            'sale_orders': sale_orders,
            'start_date': start_date,
            'end_date': end_date,
            'partners': self.env['res.partner'].browse(partner_ids),
        }
