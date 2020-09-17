from odoo import api, fields, models



class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    def _compute_best_prices(self):
        for item in self:

            po_lines = self.env['purchase.order.line'].browse(0)
            for pr_line in item.line_ids:

                po_line = self.env['purchase.order.line'].search(
                    [('product_id', '=', pr_line.product_id.id),
                     ('order_id.requisition_id', '=', item.id),
                     ('price_unit','>', 0)], 
                    limit=1, order='price_unit')
                
                po_lines |= po_line

            item.best_price_ids = po_lines

    supplier_ids = fields.Many2many('res.partner', string="Fornecedores")
    best_price_ids = fields.One2many('purchase.order.line', compute='_compute_best_prices')

    def action_generate_all_quotations(self): 
        for supplier in self.supplier_ids:
            order = self.env['purchase.order'].create({'partner_id': supplier.id, 'requisition_id': self.id})
            order._onchange_requisition_id()

            result = order.action_rfq_send()
            composer = self.env['mail.compose.message'].with_context(result['context']).create({})
            composer.onchange_template_id_wrapper()
            composer.action_send_mail()